#!/bin/sh

set -e
set -o nounset

source .branch.sh

set -x
git fetch
git checkout $PROGRAMS_BRANCH
trap "git checkout -" EXIT
git merge --ff-only origin/programs
git push origin "$PROGRAMS_BRANCH"
