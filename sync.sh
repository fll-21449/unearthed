#!/bin/bash
#/ Usage: ./sync.sh [-m MESSAGE]

set -e
set -o nounset

set -x
#mind-meld mindstorms fetch --git refs/heads/mindstorms-programs "$@"
mind-meld spike fetch --git refs/heads/programs "$@"
git push origin programs
