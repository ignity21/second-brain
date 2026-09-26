#!/usr/bin/env bash
# Build the static org-roam-ui site for GitHub Pages.
#
# Usage: publish/build.sh ORG-ROAM-UI-DIR [OUT-DIR]
#
# ORG-ROAM-UI-DIR is a checkout of ignity21/org-roam-ui (`static' branch)
# with its dependencies installed.  OUT-DIR defaults to ./site.
# BASE_PATH (default /second-brain) is the URL path the site is served under.
# Extra Emacs arguments, such as -L load paths, can be passed in EMACS_ARGS.
set -euo pipefail

repo=$(cd "$(dirname "$0")/.." && pwd)
ui=$(cd "${1:?usage: publish/build.sh ORG-ROAM-UI-DIR [OUT-DIR]}" && pwd)
out=$(realpath -m "${2:-$repo/site}")
roam="$repo/roamnotes-v2"
base_path=${BASE_PATH-/second-brain}

rm -rf "$out"
mkdir -p "$out"

# shellcheck disable=SC2086 # EMACS_ARGS is intentionally word-split.
emacs --batch ${EMACS_ARGS:-} -l "$repo/publish/export.el" "$roam" "$ui" "$out/data"

(
  cd "$ui"
  export NEXT_PUBLIC_STATIC=1 NEXT_PUBLIC_BASE_PATH="$base_path"
  # Next 11's webpack 4-era hashing needs the legacy OpenSSL provider on Node >= 17.
  export NODE_OPTIONS=--openssl-legacy-provider
  npx next build
  npx next export -o "$out/ui"
)
cp -r "$out/ui/." "$out"
rm -rf "$out/ui"

# Note resources (images, attachments), addressed by path from the roam root.
rsync -a --prune-empty-dirs \
  --exclude='.*' --exclude='logseq/' --exclude='*.org' --exclude='*.org_archive' \
  "$roam/" "$out/files/"

touch "$out/.nojekyll"
echo "Site written to $out"
