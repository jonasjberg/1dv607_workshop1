#!/usr/bin/env bash

# JOLLY PIRATE launcher script for MacOS/Linux
# ============================================
# Copyright(c) 2017 Jonas Sjöberg
# https://github.com/jonasjberg
# http://www.jonasjberg.com
# University mail: js224eh[a]student.lnu.se

set -o nounset -o pipefail


# Make sure that Python 3 is available.
if ! command -v python3 >/dev/null 2>&1
then
    cat >&2 <<EOF

[ERROR] This program requires Python v3.x to run.
        Please install python3 and make sure it is executable.

EOF
    exit 1
fi


# Check if running on a supported/target operating system.
case $OSTYPE in
    darwin*) ;;
     linux*) ;;
          *) cat >&2 <<EOF

[WARNING] Running on unsupported operating system "$OSTYPE"
          Use the launcher-script appropiate for your OS!

EOF
;;
esac


# Get the absolute path of the main module.
#
# NOTE: The version of readlink shipped with MacOS does not have the '-f'
#       option. Description from the "readlink (GNU coreutils) 8.25" manpage:
#
#       -f, --canonicalize
#       canonicalize by following every symlink in every component of
#       the given name recursively; all but the last component must exist
#
if readlink --version 2>/dev/null | grep -q 'GNU coreutils'
then
    # Using GNU coreutils version of readlink.
    JOLLYPIRATE_PATH="$(dirname -- "$(readlink -fn -- "$0")")"
else
    # Not using GNU coreutils readlink or readlink is not available.
    _abs_self_path="$(python -c "import os; print(os.path.realpath(\"$0\"))")"
    JOLLYPIRATE_PATH="$(dirname -- "${_abs_self_path}")"
fi


# Make sure that the resulting path is accessible.
(cd "$JOLLYPIRATE_PATH") 2>/dev/null 
if [ "$?" -ne "0" ]
then
    echo "[ERROR] Unable to cd to JOLLYPIRATE_PATH: \"${JOLLYPIRATE_PATH}\"" >&2
    exit 1
fi


# Execute the main module in a subshell.
(
    cd "$JOLLYPIRATE_PATH" && python3 jollypirate "$@"
)

