#!/usr/bin/env bash

# Workshop 3 launcher script for MacOS/Linux
# ==========================================
# Copyright(c) 2017 Jonas Sjöberg
# https://github.com/jonasjberg
# http://www.jonasjberg.com
# University mail: js224eh[a]student.lnu.se

set -o nounset -o pipefail

SELF_DIR="$(realpath -e "$(dirname "$0")")"


( cd "$SELF_DIR" && java -jar ./build/workshop3.jar )

