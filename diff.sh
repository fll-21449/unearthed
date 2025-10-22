#!/bin/bash
#/ Usage: ./diff.sh [spike|mindstorms]

set -e
set -o nounset

source .branch.sh

set -x
exec mind-meld $PROGRAM diff $PROGRAMS_REF
