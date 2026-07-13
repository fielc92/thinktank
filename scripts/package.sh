#!/usr/bin/env sh
set -eu

root=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
cd "$root"
version=$(cat VERSION)
archive="$root/dist/thinktank-$version.zip"

python3 scripts/validate-package.py .
bash tests/run.sh
rm -rf dist
mkdir -p dist

python3 - "$root" "$archive" <<'PY'
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

root = Path(sys.argv[1]).resolve()
archive = Path(sys.argv[2]).resolve()
exclude_dirs = {".git", "dist", "__pycache__", ".worktrees"}
exclude_suffixes = {".pyc"}

with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if path.is_dir() or any(part in exclude_dirs for part in relative.parts):
            continue
        if path.suffix in exclude_suffixes:
            continue
        info = zipfile.ZipInfo(f"thinktank-{(root / 'VERSION').read_text().strip()}/{relative.as_posix()}")
        info.date_time = (2026, 7, 12, 0, 0, 0)
        info.compress_type = zipfile.ZIP_DEFLATED
        mode = path.stat().st_mode & 0o777
        info.external_attr = mode << 16
        zf.writestr(info, path.read_bytes())

print(archive)
PY

python3 - "$archive" <<'PY'
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

archive = Path(sys.argv[1])
required = (
    "scripts/validate-package.py",
    "scripts/install-skill.sh",
    "scripts/package.sh",
    "skills/collaborating/scripts/lint-report.py",
    "tests/run.sh",
)
with zipfile.ZipFile(archive) as zf:
    prefix = zf.namelist()[0].split("/", 1)[0]
    missing_modes = []
    for relative in required:
        info = zf.getinfo(f"{prefix}/{relative}")
        mode = (info.external_attr >> 16) & 0o777
        if not mode & 0o111:
            missing_modes.append(f"{relative} ({mode:o})")
if missing_modes:
    raise SystemExit("archive lost executable modes: " + ", ".join(missing_modes))
print("Archive executable-mode metadata verified")
PY

echo "Created $archive"
