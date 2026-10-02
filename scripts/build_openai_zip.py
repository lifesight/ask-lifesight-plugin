#!/usr/bin/env python3
"""Build dist/ask-lifesight-chatgpt.zip, the package the ChatGPT Plugins dashboard takes (developers.openai.com/
plugins/deploy/submission): plugin.json and mcp.json at the root, skills/ and assets/ beside them, and nothing of
the Claude or registry files (.claude-plugin/, .mcp.json, server.json, hooks/, guidance/, docs/, README). The two
skills that make sense as a recurring task get one ChatGPT sentence in their ZIP copy only, so the skills the
repo ships to Claude Code never change (the plan's §0.4: this build is invisible to Claude). Runs the checker
first; refuses to build on a failure or a missing file. Run as `uv run --no-project --with jsonschema python -I scripts/build_openai_zip.py` (-I keeps a user
site out of the picture)."""
from __future__ import annotations

import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dist" / "ask-lifesight-chatgpt.zip"
INCLUDE_FILES = ("plugin.json", "mcp.json")
INCLUDE_DIRS = ("skills", "assets")
# the plan's sentence (CG3.1), for the two skills a member would run on a schedule; CG3.2 verifies that a plugin
# runs inside a ChatGPT scheduled task before the listing is submitted
SCHEDULED_TASK_SKILLS = ("weekly-performance-readout", "data-health")
SCHEDULED_TASK_NOTE = "\n## In ChatGPT\nSet this as a weekly task in ChatGPT.\n"


def packaged(path: Path) -> bytes:
    data = path.read_bytes()
    if path.name == "SKILL.md" and path.parent.name in SCHEDULED_TASK_SKILLS:
        data = data.rstrip(b"\n") + b"\n" + SCHEDULED_TASK_NOTE.encode()
    return data


def main() -> int:
    check = subprocess.run([sys.executable, "-I", str(ROOT / "scripts/check_openai_package.py")])
    if check.returncode != 0:
        return check.returncode
    missing = [n for n in INCLUDE_FILES if not (ROOT / n).is_file()]
    if missing:
        print(f"missing: {', '.join(missing)}")
        return 1
    OUT.parent.mkdir(exist_ok=True)
    noted = 0
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zf:
        for name in INCLUDE_FILES:
            zf.write(ROOT / name, name)
        for d in INCLUDE_DIRS:
            for p in sorted((ROOT / d).rglob("*")):
                if p.is_file() and "__pycache__" not in p.parts:
                    data = packaged(p)
                    noted += data != p.read_bytes()
                    zf.writestr(str(p.relative_to(ROOT)), data)
    if noted != len(SCHEDULED_TASK_SKILLS):
        print(f"expected the scheduled-task note on {len(SCHEDULED_TASK_SKILLS)} skills, wrote {noted}")
        return 1
    names = zipfile.ZipFile(OUT).namelist()
    print(f"wrote {OUT.relative_to(ROOT)}: {len(names)} files, {OUT.stat().st_size} bytes; "
          f"the scheduled-task note on {noted} skills")
    return 0


if __name__ == "__main__":
    sys.exit(main())
