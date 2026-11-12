#!/bin/sh
# Build the site and publish dist/ to the gh-pages branch, which GitHub Pages serves.
# Usage: npm run deploy
set -e
cd "$(dirname "$0")/.."
remote=$(git remote get-url origin)
rev=$(git rev-parse --short HEAD)
npm run build
touch dist/.nojekyll
tmp=$(mktemp -d)
cp -R dist/. "$tmp"
cd "$tmp"
git init -q -b gh-pages
git add -A
git commit -q -m "Deploy $rev"
git push -f "$remote" gh-pages
echo "Published $rev to gh-pages"
