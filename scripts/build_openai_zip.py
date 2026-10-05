#!/usr/bin/env python3
"""Build and inspect the public portable ZIP; --draft and --submission are explicit.

Requires jsonschema and PyYAML. This builds a package, never uploads or submits it.
"""
from __future__ import annotations

import argparse
import importlib.util
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dist" / "ask-lifesight-chatgpt.zip"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--draft", action="store_true", help="build for portal draft setup; review materials may be incomplete")
    mode.add_argument("--submission", action="store_true", help="also require final local review metadata; portal/live checks remain separate")
    args = parser.parse_args()
    command = [sys.executable, "-I", str(ROOT / "scripts/check_openai_package.py")]
    if args.submission:
        command.append("--submission")
    check = subprocess.run(command)
    if check.returncode:
        return check.returncode
    OUT.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as archive:
        for name in ("plugin.json", "mcp.json"):
            archive.write(ROOT / name, name)
        for directory in ("skills", "assets"):
            for path in sorted((ROOT / directory).rglob("*")):
                if path.is_file() and "__pycache__" not in path.parts:
                    archive.write(path, path.relative_to(ROOT).as_posix())
    spec = importlib.util.spec_from_file_location("openai_preflight", ROOT / "scripts/openai_preflight.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    problems = module.check_zip(OUT, submission=args.submission)
    if problems:
        OUT.unlink()
        print("\n".join(f"FAIL {p}" for p in problems))
        return 1
    with zipfile.ZipFile(OUT) as archive:
        count = len(archive.namelist())
    label = "draft" if args.draft else "local review-metadata checked"
    print(f"wrote {OUT.relative_to(ROOT)}: {count} files, {OUT.stat().st_size} bytes; {label}; production/portal checks pending")
    return 0


if __name__ == "__main__":
    sys.exit(main())
