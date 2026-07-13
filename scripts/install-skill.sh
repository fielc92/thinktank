#!/usr/bin/env sh
set -eu

usage() {
  echo "usage: $(basename "$0") [--force] TARGET_SKILLS_DIRECTORY" >&2
  exit 2
}

force=0
if [ "${1:-}" = "--force" ]; then
  force=1
  shift
fi
[ "$#" -eq 1 ] || usage

target=$1
root=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
source_dir="$root/skills/collaborating"
destination="$target/collaborating"

[ -d "$source_dir" ] || {
  echo "error: source skill not found: $source_dir" >&2
  exit 1
}

mkdir -p "$target"
if [ -e "$destination" ]; then
  if [ "$force" -ne 1 ]; then
    echo "error: destination exists: $destination (use --force to replace it)" >&2
    exit 1
  fi
  rm -rf "$destination"
fi

cp -R "$source_dir" "$destination"
echo "Installed collaborating skill to $destination"
