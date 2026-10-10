#!/usr/bin/env python3
"""Pin the harness assistant-only golden surface and regenerate its public reference.

Uses git show at an exact resolved commit; never imports or runs the harness.
Fetch the desired harness ref separately. --check compares without writing.
"""
from __future__ import annotations

import argparse
import ast
import importlib.util
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SURFACE_PATH = "tests/golden/mcp_surface.assistant-only.json"
PROFILE_SOURCE = "src/mia/mcp/profile.py"


def read_git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True)


def capture_profile(repo: Path, ref: str) -> dict:
    commit = read_git(repo, "rev-parse", "--verify", f"{ref}^{{commit}}").strip()
    surface = json.loads(read_git(repo, "show", f"{commit}:{SURFACE_PATH}"))
    tree = ast.parse(read_git(repo, "show", f"{commit}:{PROFILE_SOURCE}"))
    allowlist = None
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "ASSISTANT_ONLY"
                                                for t in node.targets) and isinstance(node.value, ast.Call):
            allowlist = next(ast.literal_eval(k.value) for k in node.value.keywords if k.arg == "listed_tools")
    names = [tool["name"] for tool in surface["tools"]]
    if allowlist is None or len(names) != len(set(names)) or set(names) != set(allowlist):
        raise ValueError("assistant-only golden surface does not match the production allowlist")
    return {"profile": "assistant-only", "source": {
        "repository": "https://github.com/Lifesight-Software-Pvt-Ltd/lifesight-platform-mia-agents",
        "commit": commit, "path": SURFACE_PATH,
        "surface_sha256": preflight.surface_digest(surface),
    }, "surface": surface}


spec = importlib.util.spec_from_file_location("preflight", ROOT / "scripts/openai_preflight.py")
preflight = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preflight)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--harness-repo", required=True, type=Path)
    parser.add_argument("--ref", default="origin/main")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    profile = capture_profile(args.harness_repo, args.ref)
    files = {preflight.PROFILE_PATH: json.dumps(profile, indent=2) + "\n",
             ROOT / "docs/TOOLS.md": preflight.render_tool_reference(profile)}
    if args.check:
        stale = [str(p.relative_to(ROOT)) for p, text in files.items() if not p.is_file() or p.read_text() != text]
        if stale:
            print("FAIL production profile/reference differs from harness ref: " + ", ".join(stale))
            return 1
    else:
        for path, text in files.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
    print(f"{'checked' if args.check else 'pinned'} assistant-only: {len(profile['surface']['tools'])} tools "
          f"from harness {profile['source']['commit']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
