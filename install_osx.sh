#!/bin/bash

set -o nounset
set -o errexit

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SCRIPT_NAME="ConsoleControlSurface"

LIVE_SCRIPTS_DIR="/Applications/Ableton Live 10 Suite.app/Contents/App-Resources/MIDI Remote Scripts"

cd "${LIVE_SCRIPTS_DIR}"
sudo ln -sfn "${SCRIPT_DIR}/${SCRIPT_NAME}"

echo "Installed into '${LIVE_SCRIPTS_DIR}/${SCRIPT_NAME}'"
