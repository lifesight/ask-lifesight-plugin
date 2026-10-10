#!/usr/bin/env python3
"""The ChatGPT plugin package against the local package checks (developers.openai.com/plugins, read 2026-10-02):
the agent-plugins.org schemas (vendored in scripts/schemas/), the listing fields' character limits, the HTTPS
URLs, the asset rules (square, 48 px or more), the control-character rule, the skill sizes, the version the two
plugin manifests share, and the copy rules the guidelines state (no "MCP" or "Plugin" in the name, no pricing
language, nothing steering the model, no figure in model-visible prose). Exit 1 on any failure; the ZIP is
built only after it. Needs `jsonschema` and `PyYAML`: `uv run --no-project --with jsonschema --with pyyaml python -I scripts/check_openai_package.py`.
With `--submission` it also demands what the dashboard requires at MCP review and the listing cannot carry until the
owner has them: `review.demo_recording_url` (CG3.4). Country declarations in the ZIP are optional; verify targeting in the portal."""
from __future__ import annotations

import importlib.util
import json
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIMITS = {"displayName": 30, "shortDescription": 30, "longDescription": 4000, "developerName": 80}
URL_FIELDS = ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL")
COPY_FIELDS = ("displayName", "shortDescription", "longDescription")
SERVER_URL = "https://ask.lifesight.io/mcp"
# "promotion" is the product's own word for making a plan the workspace default (no money moves); the guideline's
# "promotions" are marketing offers, caught here by their offer words (promo, promotional offer, special offer)
PRICING = re.compile(
    r"\b(price|prices|pricing|subscription|subscribe|free trial|trial|discount|promo|promotional offer|special offer"
    r"|upgrade|premium|tier|paid|pay|fee|fees|cost|costs|enterprise plan|pricing plan)\b", re.I)
STEERING = re.compile(
    r"\b(prefer|preferred|instead of|rather than|better than|best|recommended|official|always use|only use"
    r"|do not use other|the only)\b", re.I)
FIGURE = re.compile(r"\d")  # listing copy is model-visible prose and carries no figure of any kind
CONTROL = re.compile(r"[\x00-\x08\x09\x0b-\x1f\x7f]")  # tabs and other control characters are rejected; newlines stay
COUNTRY = re.compile(r"^[A-Z]{2}$")
REVIEW_COUNTS = {"positive": 5, "negative": 3}  # EXACTLY these for the initial MCP review (submission page, 2026-10-02)
REVIEW_TEXT_MAX = 4000
POSITIVE_FIELDS = ("description", "prompt", "tools_triggered", "expected_behavior")
NEGATIVE_FIELDS = ("description", "prompt")


def fail(msg: str, problems: list[str]) -> None:
    problems.append(msg)


def validate_schema(instance: dict, schema_path: Path, problems: list[str], label: str) -> None:
    import jsonschema  # a missing module is a crash, never a silent pass (the system python lacks it)

    try:
        jsonschema.validate(instance, json.loads(schema_path.read_text()))
    except jsonschema.ValidationError as exc:
        fail(f"{label}: schema: {exc.message}", problems)


def image_square_at_least_48(path: Path) -> str | None:
    """None when the image is square and 48 px or more (SVG by viewBox or width/height; PNG by IHDR; JPEG and
    WebP are accepted by extension only), else the reason."""
    suffix = path.suffix.lower()
    if suffix == ".svg":
        text = path.read_text(errors="replace")
        m = re.search(r'viewBox="\s*[-\d.]+[\s,]+[-\d.]+[\s,]+([\d.]+)[\s,]+([\d.]+)\s*"', text)
        if not m:
            m = re.search(r'width="([\d.]+)(?:px)?"[^>]*height="([\d.]+)(?:px)?"', text)
        if not m:
            return "SVG needs a square numeric viewBox or width and height"
        w, h = float(m.group(1)), float(m.group(2))
    elif suffix == ".png":
        head = path.read_bytes()[:24]
        if head[:8] != b"\x89PNG\r\n\x1a\n" or head[12:16] != b"IHDR":
            return "not a PNG"
        w, h = struct.unpack(">II", head[16:24])
        if max(w, h) > 4096:
            return "raster images are at most 4096 px in either dimension"
    else:
        return None
    if w != h:
        return f"must be square, is {w:g} by {h:g}"
    if w < 48:
        return f"must be at least 48 px, is {w:g}"
    return None


def check_review(openai: dict, problems: list[str], *, submission: bool, names: set[str]) -> None:
    """`extensions.com.openai.review` (fields and counts from the submission page, read 2026-10-02): exactly five
    positive cases with a description, a prompt, the tools expected (a comma-separated string) and the observable
    behaviour; exactly three negative cases with a
    description and a prompt; the commerce declaration; every text figure-free and free of control characters; the
    expected tools real. The demo recording URL is required at MCP review, so only `--submission` demands it."""
    review = openai.get("review")
    if review is None:
        if submission:
            fail("review: the submission needs extensions.com.openai.review (test cases, demo recording)", problems)
        return
    cases = review.get("test_cases", {})
    for kind, count in REVIEW_COUNTS.items():
        items = cases.get(kind, [])
        if len(items) != count:
            fail(f"review.test_cases.{kind}: exactly {count} for the initial MCP review, {len(items)} given", problems)
        fields = POSITIVE_FIELDS if kind == "positive" else NEGATIVE_FIELDS
        for i, case in enumerate(items, start=1):
            for field in fields:
                if not case.get(field):
                    fail(f"review.test_cases.{kind}[{i}] missing {field}", problems)
            for field in ("description", "prompt", "expected_behavior"):
                text = str(case.get(field) or "")
                if len(text) > REVIEW_TEXT_MAX:
                    fail(f"review.test_cases.{kind}[{i}].{field} is {len(text)} chars; limit {REVIEW_TEXT_MAX}", problems)
                if FIGURE.search(text):
                    fail(f"review.test_cases.{kind}[{i}].{field} carries a figure: {FIGURE.search(text).group(0)!r}", problems)
                if CONTROL.search(text):
                    fail(f"review.test_cases.{kind}[{i}].{field} carries a control character", problems)
            triggered = case.get("tools_triggered")
            if isinstance(triggered, list):  # the page documents a comma-separated STRING; an array is not the shape
                fail(f"review.test_cases.{kind}[{i}].tools_triggered must be a comma-separated string, not an array", problems)
                triggered = ", ".join(map(str, triggered))
            for tool in [t.strip() for t in str(triggered or "").split(",") if t.strip()]:
                if tool not in names:
                    fail(f"review.test_cases.{kind}[{i}] names a tool unavailable in production: {tool!r}", problems)
            if kind == "negative" and case.get("tools_triggered"):
                fail(f"review.test_cases.negative[{i}] expects a tool; a negative expects none", problems)
    if not isinstance(review.get("commerce"), bool):
        fail("review.commerce must be declared true or false", problems)
    url = str(review.get("demo_recording_url") or "")
    if url and (not url.startswith("https://") or len(url) > 1024):
        fail(f"review.demo_recording_url must be an https URL under 1024 chars: {url!r}", problems)
    if submission and not url:
        fail("review.demo_recording_url is required for MCP review (the owner's video)", problems)


def main(argv: list[str] | None = None) -> int:
    submission = "--submission" in (argv if argv is not None else sys.argv[1:])
    problems: list[str] = []
    spec = importlib.util.spec_from_file_location("openai_preflight", ROOT / "scripts/openai_preflight.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    problems.extend(module.check_source(ROOT, submission=submission))
    problems.extend(module.check_tool_reference(ROOT))
    if problems:
        print("\n".join(f"FAIL {p}" for p in problems))
        return 1
    manifest = json.loads((ROOT / "plugin.json").read_text())
    mcp = json.loads((ROOT / "mcp.json").read_text())
    claude = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
    validate_schema(manifest, ROOT / "scripts/schemas/plugin.schema.json", problems, "plugin.json")
    validate_schema(mcp, ROOT / "scripts/schemas/mcp.schema.json", problems, "mcp.json")
    if manifest.get("version") != claude.get("version"):
        fail(f"plugin.json version {manifest.get('version')!r} differs from .claude-plugin/plugin.json "
             f"{claude.get('version')!r}: one plugin, one version", problems)
    if re.search(r"\b(ChatGPT|Claude|Codex)\b", manifest.get("description", "")):
        fail("plugin.json description is the portable identity (ChatGPT and Codex read it): name no host", problems)
    openai = manifest.get("extensions", {}).get("com.openai", {})
    if "apps" in manifest or (ROOT / ".app.json").exists():
        fail("a ZIP with app references (apps / .app.json) cannot be submitted; mcp.json is the route", problems)
    iface = openai.get("interface", {})
    for field, limit in LIMITS.items():
        value = str(iface.get(field, ""))
        if not value:
            fail(f"interface.{field} missing", problems)
        elif len(value) > limit:
            fail(f"interface.{field} is {len(value)} chars; limit {limit}", problems)
    for field in URL_FIELDS:
        url = str(iface.get(field, ""))
        if not url.startswith("https://") or len(url) > 1024:
            fail(f"interface.{field} must be an https URL under 1024 chars: {url!r}", problems)
    caps = iface.get("capabilities", [])
    if len(caps) > 20 or any(len(c) > 120 for c in caps):
        fail("capabilities: at most 20, each at most 120 chars", problems)
    prompts = iface.get("defaultPrompt", [])
    if len(prompts) > 3 or any(len(p) > 128 for p in prompts):
        fail("defaultPrompt: at most three, each at most 128 chars", problems)
    name = iface.get("displayName", "")
    if re.search(r"\b(MCP|Plugin)\b", name, re.I):
        fail(f"displayName must not say MCP or Plugin: {name!r}", problems)
    if re.search(r"\b(ChatGPT|Claude|Codex)\b", iface.get("longDescription", "")):
        fail("longDescription names a host; the listing is shared by ChatGPT and Codex", problems)
    copy = [(f, str(iface.get(f, ""))) for f in COPY_FIELDS]
    copy += [("capabilities", c) for c in caps] + [("defaultPrompt", p) for p in prompts]
    for field, text in copy:
        for rule, label in ((PRICING, "carries pricing language"), (STEERING, "steers the model"),
                            (FIGURE, "carries a figure (model-visible prose is not provenance)"),
                            (CONTROL, "carries a tab or control character")):
            hit = rule.search(text)
            if hit:
                fail(f"interface.{field} {label}: {hit.group(0)!r}", problems)
    for kw in manifest.get("keywords", []):
        if kw.lower() not in iface.get("longDescription", "").lower():
            fail(f"keyword {kw!r} is not in the description (docs/CHATGPT_LISTING.md says each is)", problems)
    for field in ("logo", "composerIcon"):
        rel = str(iface.get(field, ""))
        path = ROOT / rel
        if not rel.startswith("./") or not path.is_file():
            fail(f"interface.{field} must be a relative path to a file in the package: {rel!r}", problems)
        elif path.stat().st_size > 5 * 1024 * 1024 or path.suffix.lower() not in (".png", ".jpg", ".jpeg", ".webp", ".svg"):
            fail(f"interface.{field}: PNG, JPEG, WebP or SVG under 5 MiB", problems)
        else:
            why = image_square_at_least_48(path)
            if why:
                fail(f"interface.{field} {rel}: {why}", problems)
    for rel in iface.get("screenshots", []):
        if not (ROOT / rel).is_file():
            fail(f"screenshot missing: {rel}", problems)
    publication = openai.get("publication", {})
    for code in publication.get("countries", []):
        if not COUNTRY.match(str(code)):
            fail(f"publication.countries: uppercase two-letter country codes only: {code!r}", problems)
    notes = str(publication.get("release_notes") or "")
    if FIGURE.search(notes) or CONTROL.search(notes):
        fail("publication.release_notes carries a figure or a control character", problems)
    check_review(openai, problems, submission=submission, names=module.production_tool_names())
    server = mcp["mcpServers"].get("ask-lifesight", {})
    if server.get("url") != SERVER_URL or server.get("type") != "streamable-http":
        fail(f"mcp.json must name the listed server {SERVER_URL} over streamable-http: {server}", problems)
    skills = sorted(p for p in (ROOT / "skills").iterdir() if p.is_dir())
    if not skills:
        fail("no skills", problems)
    for skill in skills:
        md = skill / "SKILL.md"
        if not md.is_file():
            fail(f"{skill.name}: no SKILL.md", problems)
            continue
        text = md.read_text()
        front = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        keys = set(re.findall(r"^([a-z-]+):", front.group(1), re.M)) if front else set()
        if not {"name", "description"} <= keys:
            fail(f"{skill.name}: SKILL.md frontmatter needs name and description", problems)
        if md.stat().st_size > 256 * 1024:
            fail(f"{skill.name}: SKILL.md over 256 KiB", problems)
        files = [p for p in skill.rglob("*") if p.is_file()]
        if len(files) > 100:
            fail(f"{skill.name}: over 100 files", problems)
        if any(p.stat().st_size > 1024 * 1024 for p in files):
            fail(f"{skill.name}: a file over 1 MiB", problems)
        if sum(p.stat().st_size for p in files) > 5 * 1024 * 1024:
            fail(f"{skill.name}: over 5 MiB in all", problems)
    if problems:
        print("\n".join(f"FAIL {p}" for p in problems))
        return 1
    review = openai.get("review", {}).get("test_cases", {})
    print(f"ok: plugin.json ({len(iface['longDescription'])}/4000 description chars, "
          f"{len(iface['shortDescription'])}/30 subtitle chars, {len(review.get('positive', []))} positive and "
          f"{len(review.get('negative', []))} negative review cases), mcp.json, {len(skills)} skills, assets"
          + ("; local review-metadata checks passed; production/portal checks pending" if submission else "; draft package checks passed"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
