"""Additional public-package checks; portal scans and production behavior remain separate.

Sources checked 2026-10-05: developers.openai.com/plugins/deploy/submission,
submission-errors, build/plugins, build/skills and plugin-guidelines.
Requires PyYAML; Pillow is required only when raster branding is present.
"""
from __future__ import annotations

import json
import math
import re
import stat
import unicodedata
import zipfile
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree

CATEGORIES = {
    "Productivity", "Creativity", "Developer Tools", "Business & Operations", "Data & Analytics",
    "Communication", "Education & Research", "Security", "Finance", "Healthcare",
    "Travel", "Entertainment", "Other",
}
COUNTRIES = set("""AD AE AF AG AI AL AM AO AQ AR AS AT AU AW AX AZ BA BB BD BE BF BG BH BI BJ BL BM BN BO BQ BR BS BT BV BW BY BZ CA CC CD CF CG CH CI CK CL CM CN CO CR CU CV CW CX CY CZ DE DJ DK DM DO DZ EC EE EG EH ER ES ET FI FJ FK FM FO FR GA GB GD GE GF GG GH GI GL GM GN GP GQ GR GS GT GU GW GY HK HM HN HR HT HU ID IE IL IM IN IO IQ IR IS IT JE JM JO JP KE KG KH KI KM KN KP KR KW KY KZ LA LB LC LI LK LR LS LT LU LV LY MA MC MD ME MF MG MH MK ML MM MN MO MP MQ MR MS MT MU MV MW MX MY MZ NA NC NE NF NG NI NL NO NP NR NU NZ OM PA PE PF PG PH PK PL PM PN PR PS PT PW PY QA RE RO RS RU RW SA SB SC SD SE SG SH SI SJ SK SL SM SN SO SR SS ST SV SX SY SZ TC TD TF TG TH TJ TK TL TM TN TO TR TT TV TW TZ UA UG UM US UY UZ VA VC VE VG VI VN VU WF WS YE YT ZA ZM ZW""".split())
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
                    r"(?:-(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)(?:\.(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*)?"
                    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$")


def text_ok(value: object, maximum: int, *, multiline: bool = False) -> bool:
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        return False
    return all((multiline and c == "\n") or unicodedata.category(c) not in {"Cc", "Cf", "Zl", "Zp"}
               for c in value)


def https_ok(value: object, maximum: int = 1024) -> bool:
    if not text_ok(value, maximum) or any(c.isspace() for c in value):
        return False
    try:
        parsed = urlsplit(value)
        return parsed.scheme == "https" and bool(parsed.hostname) and parsed.username is None and parsed.password is None
    except ValueError:
        return False


def asset_path(root: Path, value: object) -> Path | None:
    if not isinstance(value, str) or value != value.strip() or not value.startswith("./"):
        return None
    if "\\" in value or ".." in value.split("/") or not text_ok(value, 4096):
        return None
    path = root / value
    if path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(root.resolve()):
        return None
    return path


def image_error(path: Path) -> str | None:
    if path.stat().st_size > 5 * 1024 * 1024:
        return "over 5 MiB"
    if path.suffix.lower() == ".svg":
        try:
            svg = ElementTree.fromstring(path.read_text(encoding="utf-8"))
            if svg.tag.split("}")[-1] != "svg":
                return "root is not svg"
            if "viewBox" in svg.attrib:
                x, y, w, h = map(float, re.split(r"[\s,]+", svg.attrib["viewBox"].strip()))
                if not all(math.isfinite(n) for n in (x, y)):
                    return "nonfinite viewBox"
            else:
                w, h = float(svg.attrib["width"]), float(svg.attrib["height"])
            if not all(math.isfinite(n) for n in (w, h)) or w != h or w < 48:
                return "square finite numeric dimensions of at least 48 required"
        except (ElementTree.ParseError, UnicodeError, ValueError, KeyError):
            return "malformed XML or missing/invalid numeric dimensions"
    else:
        formats = {".png": "PNG", ".jpg": "JPEG", ".jpeg": "JPEG", ".webp": "WEBP"}
        if path.suffix.lower() not in formats:
            return "unsupported image format"
        try:
            from PIL import Image
        except ImportError:
            return "install Pillow to verify raster decoding and actual dimensions"
        try:
            with Image.open(path) as image:
                w, h = image.size
                if image.format != formats[path.suffix.lower()]:
                    return "extension/content mismatch"
                if w != h or w < 48 or w > 4096:
                    return "square raster dimensions between 48 and 4096 required"
                image.verify()
        except Exception:
            return "raster image cannot be decoded safely"
    return None


def _unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def check_source(root: Path, *, submission: bool = False) -> list[str]:
    import yaml

    problems: list[str] = []

    def require(condition, message):
        if not condition:
            problems.append(message)

    try:
        manifest = json.loads((root / "plugin.json").read_text(), object_pairs_hook=_unique_pairs)
        mcp = json.loads((root / "mcp.json").read_text(), object_pairs_hook=_unique_pairs)
        if not isinstance(manifest, dict) or not isinstance(mcp, dict):
            raise ValueError("JSON root must be an object")
        openai = manifest.get("extensions", {}).get("com.openai", {})
        iface = openai.get("interface", {})
        if not isinstance(openai, dict) or not isinstance(iface, dict):
            raise ValueError("OpenAI extension/interface must be objects")
    except (OSError, UnicodeError, ValueError, AttributeError, TypeError):
        return ["public manifests must be readable JSON objects with unique keys and valid extension objects"]
    require(text_ok(manifest.get("name"), 64) and bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", str(manifest.get("name")))), "package name: use lowercase letters/digits and single hyphens")
    require(text_ok(manifest.get("version"), 64) and bool(SEMVER.fullmatch(str(manifest.get("version")))), "package version: explicit semantic version required")
    for layer in (manifest, openai):
        require(not any(layer.get(key) is not None for key in ("apps", "hooks")), "public upload cannot declare app bindings or lifecycle hooks")
    for field, maximum in {"displayName": 30, "shortDescription": 30, "longDescription": 4000, "developerName": 80}.items():
        require(text_ok(iface.get(field), maximum, multiline=field == "longDescription"), f"interface.{field}: nonblank supported text within limit required")
    require(isinstance(iface.get("category"), str) and iface.get("category") in CATEGORIES, "interface.category: recognized category required")
    for field in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
        require(https_ok(iface.get(field)), f"interface.{field}: HTTPS host without credentials/whitespace required")
    for field, maximum, count in (("capabilities", 120, 20), ("defaultPrompt", 128, 3)):
        values = iface.get(field, [])
        if field == "defaultPrompt" and isinstance(values, str):
            values = [values]
        require(isinstance(values, list) and len(values) <= count, f"interface.{field}: invalid list/count")
        if not isinstance(values, list):
            continue
        require(all(text_ok(value, maximum) for value in values), f"interface.{field}: nonblank single-line strings within limit required")
        if field == "defaultPrompt":
            normalized = [" ".join(unicodedata.normalize("NFKC", value).casefold().split()) for value in values if isinstance(value, str)]
            require(len(normalized) == len(set(normalized)), "defaultPrompt: duplicates after Unicode/whitespace normalization")
            require(all("@" not in value for value in values if isinstance(value, str)), "defaultPrompt: omit MCP mentions")
    for field, background in (("brandColor", "ffffff"), ("brandColorDark", "212121")):
        if field not in iface:
            continue
        value = iface[field]
        if not isinstance(value, str) or not re.fullmatch(r"#[\da-fA-F]{6}", value):
            problems.append(f"{field}: #RRGGBB required")
            continue
        def luminance(hex_value):
            rgb = [int(hex_value[i:i+2], 16) / 255 for i in (0, 2, 4)]
            linear = [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in rgb]
            return sum(c * k for c, k in zip(linear, (.2126, .7152, .0722)))
        a, b = sorted((luminance(value[1:]), luminance(background)))
        require((b + .05) / (a + .05) >= 2, f"{field}: contrast below 2:1")
    for field in ("logo", "composerIcon", "logoDark", "composerIconDark"):
        if field not in iface and field in ("logoDark", "composerIconDark"):
            continue
        path = asset_path(root, iface.get(field))
        if path is None:
            problems.append(f"{field}: contained ./ path to a regular file required")
        else:
            error = image_error(path)
            require(error is None, f"{field}: {error}")
    require(not iface.get("screenshots"), "screenshots require a portal scan reporting UI; this package has no UI template")
    servers = mcp.get("mcpServers", {})
    require(isinstance(servers, dict) and len(servers) == 1, "this review package requires exactly one MCP server")
    if isinstance(servers, dict):
        for name, server in servers.items():
            require(text_ok(name, 128) and isinstance(server, dict), "invalid MCP server declaration")
            if isinstance(server, dict):
                require(server.get("type") == "streamable-http" and https_ok(server.get("url")), "public MCP must use a remote HTTPS streamable-http endpoint")
                require(not any(k in server for k in ("headers", "env", "command")), "public MCP config must not carry runtime credentials or local commands")
                require(not server.get("extensions", {}).get("com.openai", {}).get("review"), "one-server review cases must have only the plugin-level declaration")
    review = openai.get("review", {})
    publication = openai.get("publication", {})
    if not isinstance(review, dict) or not isinstance(publication, dict):
        return problems + ["review/publication must be objects"]
    require(not any(k in review for k in ("test_credentials", "reviewer_instructions")), "reviewer access belongs only in the secure portal fields")
    cases = review.get("test_cases", {})
    if not isinstance(cases, dict):
        return problems + ["review.test_cases must be an object"]
    for kind, count in (("positive", 5), ("negative", 3)):
        items = cases.get(kind, [])
        require(isinstance(items, list), f"{kind} review cases must be a list")
        if not isinstance(items, list):
            continue
        if submission:
            require(len(items) == count, f"{kind}: exactly {count} review cases required")
        fields = ("description", "prompt", "tools_triggered", "expected_behavior") if kind == "positive" else ("description", "prompt")
        for case in items:
            require(isinstance(case, dict), f"{kind} review case must be an object")
            if not isinstance(case, dict):
                continue
            for field in fields:
                require(text_ok(case.get(field), 4000, multiline=True), f"{kind}.{field}: nonblank string required")
            for field in ("expected_output_url",):
                if field in case:
                    require(https_ok(case[field]), f"{kind}.{field}: valid HTTPS URL required")
            if "file_attachment_urls" in case:
                urls = case["file_attachment_urls"]
                require(isinstance(urls, list) and all(https_ok(x) for x in urls), f"{kind}: valid attachment URLs required")
    if "demo_recording_url" in review:
        require(https_ok(review["demo_recording_url"]), "demo_recording_url: valid HTTPS URL required")
    elif submission:
        problems.append("demo_recording_url: missing; actual accessible recording required for review")
    if submission:
        require(text_ok(publication.get("release_notes"), 4000, multiline=True), "release_notes: required for initial MCP review")
    if "countries" in publication:
        countries = publication["countries"]
        require(isinstance(countries, list) and all(isinstance(c, str) and c in COUNTRIES for c in countries), "countries: recognized uppercase ISO country codes required when supplied")
    if "onboardingSkill" in openai:
        require(asset_path(root, openai["onboardingSkill"]) is not None, "onboardingSkill must name a packaged regular file")
    for directory in (root / "skills", root / "assets"):
        if directory.is_symlink():
            problems.append(f"{directory.name}: public component cannot be a symlink")
        for path in directory.rglob("*"):
            if path.is_symlink() or not (path.is_file() or path.is_dir()):
                problems.append(f"{path.relative_to(root)}: public component must be a regular file/directory")
    names: set[str] = set()
    skills = root / "skills"
    require(skills.is_dir(), "skills directory missing")
    if skills.is_dir():
        for skill in sorted(skills.iterdir()):
            if not skill.is_dir() or skill.name.startswith(".") or skill.is_symlink():
                problems.append(f"{skill.name}: immediate regular skill directory required")
                continue
            md = skill / "SKILL.md"
            try:
                content = md.read_text(encoding="utf-8")
                front = re.fullmatch(r"---\r?\n(.*?)\r?\n---\r?\n(.*)", content, re.S)
                if front is None or md.is_symlink():
                    raise ValueError("missing front matter or irregular manifest")
                data = yaml.safe_load(front[1])
                if not isinstance(data, dict):
                    raise ValueError("YAML must be a mapping")
            except (OSError, UnicodeError, ValueError, yaml.YAMLError):
                problems.append(f"{skill.name}: invalid YAML front matter or unreadable SKILL.md")
                continue
            name = data.get("name")
            require(text_ok(name, 64) and len(f"{manifest.get('name')}:{name}") <= 64, f"{skill.name}: invalid/overlong skill identity")
            require(text_ok(data.get("description"), 1024, multiline=True), f"{skill.name}: invalid description")
            require(bool(front[2].strip()), f"{skill.name}: empty instructions")
            if isinstance(name, str):
                require(name not in names, f"{skill.name}: duplicate skill identity")
                names.add(name)
            require(not any(p != md for p in skill.rglob("SKILL.md")), f"{skill.name}: nested skill manifest")
    return problems


def check_zip(path: Path, *, submission: bool = False) -> list[str]:
    problems: list[str] = []
    if path.stat().st_size > 100_000_000:
        return ["archive exceeds 100 MB"]
    try:
        with zipfile.ZipFile(path) as archive:
            infos = archive.infolist()
            if not infos or len(infos) > 5000 or sum(i.file_size for i in infos) > 512 * 1024 * 1024:
                problems.append("archive entry count/uncompressed size invalid")
            normalized: set[str] = set()
            for info in infos:
                name = info.filename
                parts = name.rstrip("/").split("/")
                key = unicodedata.normalize("NFKC", name.rstrip("/")).casefold()
                mode = stat.S_IFMT(info.external_attr >> 16)
                if (not name or name != name.strip() or "\\" in name or name.startswith("/")
                        or ":" in parts[0] or any(p in ("", ".", "..") for p in parts) or len(parts) > 20
                        or any(unicodedata.category(c) in {"Cc", "Cf", "Zl", "Zp"} for c in name)):
                    problems.append(f"unsafe archive path: {name!r}")
                if key in normalized:
                    problems.append(f"duplicate/normalized collision: {name!r}")
                normalized.add(key)
                if mode not in (0, stat.S_IFREG, stat.S_IFDIR) or info.flag_bits & 1 or info.compress_type not in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED):
                    problems.append(f"unsupported/encrypted archive member: {name!r}")
                if info.file_size > 100 * 1024 * 1024:
                    problems.append(f"archive member exceeds 100 MiB: {name!r}")
                if parts[0] in (".app.json", "hooks", ".git", ".claude-plugin", ".codex-plugin"):
                    problems.append(f"public upload includes unsupported/private component: {name!r}")
            entries = {unicodedata.normalize("NFKC", i.filename.rstrip("/")).casefold(): i for i in infos}
            for key in entries:
                for depth in range(1, len(key.split("/"))):
                    parent = "/".join(key.split("/")[:depth])
                    if parent in entries and not entries[parent].is_dir():
                        problems.append("archive file/directory conflict")
                        break
            if not problems and archive.testzip() is not None:
                problems.append("archive CRC validation failed")
            if not problems:
                from tempfile import TemporaryDirectory
                with TemporaryDirectory(prefix="openai-preflight-") as folder:
                    archive.extractall(folder)
                    problems.extend(check_source(Path(folder), submission=submission))
    except (OSError, zipfile.BadZipFile, RuntimeError):
        problems.append("archive cannot be read safely")
    return problems
