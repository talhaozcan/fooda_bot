#!/usr/bin/env bash
set -eux

# Have pipreqs and pip-tools installed
# This script passes flags to pip-compile. Example:
#
#     update_requirements.sh --upgrade  # get the newest of everything
#

HERE="$(realpath "$0" | xargs dirname)"
export CUSTOM_COMPILE_COMMAND="bash $(basename $0)"
REQUIREMENTS_TXT="${HERE}/requirements.txt"

PIPCOMPILE_FLAGS=( $@ )

pipreqs "${HERE}" --print | pip-compile "${PIPCOMPILE_FLAGS[@]}" --output-file="${REQUIREMENTS_TXT}" -
