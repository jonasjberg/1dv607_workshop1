#!/usr/bin/env bash
# ______________________________________________________________________________
#
#   1DV607 Objectorienterad Analysis och Design med UML
#   Workshop 1 --- "Domain Modeling"
#
#  Author:  Jonas Sjöberg
#           Linnaeus University
#           js224eh@student.lnu.se
#           https://github.com/jonasjberg
#
# License:  Creative Commons Attribution 4.0 International (CC BY 4.0)
#           <http://creativecommons.org/licenses/by/4.0/legalcode>
#           See LICENSE.md for additional licensing information.
# ______________________________________________________________________________

set -o noclobber -o nounset -o pipefail


TEX_MAIN="${1:-}"

SCRIPT_PATH="$(cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)"
SCRIPT_NAME="$(basename $0)"
#PDF_VIEWER="xdg-open"
PDF_VIEWER="evince"

# Check that notify-send is available early on.
unset HAS_NOTIFY
command -v "notify-send" >/dev/null 2>&1 && HAS_NOTIFY="true"

# Check that icons are available. Defaults to empty icon paths -- no icons.
ICON_GOOD="/usr/share/icons/Adwaita/scalable/emotes/emote-love-symbolic.svg"
[ -e "$ICON_GOOD" ] || unset ICON_GOOD
ICON_BAD="/usr/share/icons/Adwaita/scalable/emotes/face-sick-symbolic.svg"
[ -e "$ICON_BAD" ] || unset ICON_BAD
ICON_INFO="/usr/share/icons/Adwaita/scalable/emotes/face-devilish-symbolic.svg"
[ -e "$ICON_INFO" ] || unset ICON_INFO


# Settings used when running notify-send:
NOTIFY_TIMEOUT="3000"                   # duration of message in microseconds
NOTIFY_URGENCY="normal"                 # either 'low', 'normal' or 'critical'


function msg_notify()
{
    if [ -z "$HAS_NOTIFY" ]
    then
        return 1
    fi

    if [ $# -gt 1 ];
    then
        local code="$1"
        shift
    fi
    # TODO: Shift parameter only if the first parameter is a <code> ..
    #       Currently, the first word is swallowed if <code> is null.
        
    local text="${@}"
    local icon=""

    case "$code" in
        1  ) icon=$ICON_BAD
             label="$SCRIPT_NAME FAILED!"    ;;
        0  ) icon=$ICON_GOOD
             label="$SCRIPT_NAME SUCCEEDED!" ;;
        -1 ) icon=$ICON_INFO
             label="$SCRIPT_NAME"            ;;
        *  ) icon=$ICON_INFO
             label="$SCRIPT_NAME"            ;;
    esac

    notify-send --icon="$icon"                  \
                --expire-time="$NOTIFY_TIMEOUT" \
                --urgency=normal                \
                "$label" "$(echo "${text}")"
}

markdowntoprettypdf() 
{
    src="$1"
    dest="${1%.*}.pdf"

    # Do character replacements before piping to pandoc.
    cat "$src" | sed 's/➡/-->/' | \
    pandoc --smart --normalize --standalone \
           --highlight-style=monochrome \
           --variable mainfont="DejaVu Sans" \
           --variable monofont="DejaVu Sans Mono" \
           --variable fontsize=11pt \
           --variable geometry:"top=1.5cm, bottom=2.5cm, left=1.5cm, right=1.5cm" \
           --variable geometry:a4paper \
           --number-sections \
           -f markdown \
           -o "$dest"
}


# Run all this stuff in a sub-shell because reasons.
(
  cd "$SCRIPT_PATH"
  echo "now working from directory: \"$(pwd -P)\""
  
  # First use pandoc to make pdf from the markdown files.
  # for arg in use-case-*.md
  # do
  #     markdowntoprettypdf "$arg"
  # done

  # Then copy figures from another repo ..
  # ./copy-figures.sh
  
  # Find main tex file not specified as first argument to this script.
  if [ -z "$TEX_MAIN" ]
  then
      TEX_MAIN="$(find "$SCRIPT_PATH" -type f -name "main.tex" | head -n 1)"
  fi
  
  # Do the actual thing with latexmk.
  # Run three times just to make sure..
  MKCMD="latexmk $TEX_MAIN -outdir=build -pdf -pdflatex="pdflatex\ -synctex=1\ -interaction=nonstopmode\ -shell-escape""
  ${MKCMD};
  ${MKCMD};
  ${MKCMD};
  mkcmd_result="$?"
  
  # Check if overall success with a bad, unreliable check. 
  # Need to study latexmk functionality to make this (entire script) better.
  if [ "$mkcmd_result" -eq 0 ]
  then
      msg_notify 0 "Compilation COMPLETED SUCCESSFULLY!\nlatexmk returned: $mkcmd_result"
  
      # Grab first pdf file in the build directory. Could be wrong but hey.
      pdf_file=$(find ./build -type f -name "*.pdf" | head -n 1)
  
      # Check if the pdf file is open somewhere.
      pdf_file_is_open=$(ps aux | grep "$pdf_file" | grep -v grep)
  
      # Open with viewer if not already open.
      if [ -z "$pdf_file_is_open" ]
      then
          msg_notify -1 "Opening pdf file with \"$PDF_VIEWER\" .."
          $PDF_VIEWER "$pdf_file" 2>/dev/null &
      else
          msg_notify -1 "pdf (probably) updated on disk"
      fi
  else
      msg_notify 1 "Compilation FAILED!\nlatexmk returned: $mkcmd_result"
  fi
)


if [ $? -ne 0 ]
then
    msg_notify 1 "FAILED! something somewhere returned non-zero at some point"
else
    exit 0
fi
