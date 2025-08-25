#!/bin/bash
#/ Usage: ./diff.sh [spike|mindstorms]

set -e
set -o nounset

program=spike
ref=refs/heads/programs
if [ $# -gt 0 ] && [ "$1" = mindstorms ]; then
  program=mindstorms
  ref=refs/heads/mindstorms-programs
fi

set -x
exec mind-meld $program diff $ref
