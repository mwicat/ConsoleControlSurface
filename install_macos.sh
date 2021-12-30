#!/bin/bash

set -o nounset
set -o errexit

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

LIVE_SCRIPTS_DIR="$HOME/Music/Ableton/User Library/Remote Scripts"

function install_script {
    script_name="$1"
    source_path="${SCRIPT_DIR}/${script_name}"
    target_path="${LIVE_SCRIPTS_DIR}/${script_name}"
    if [ -e "$target_path" ]; then
        echo "Target path '$target_path' already exists"
        file "$target_path"
        return
    fi
    sudo ln -sfn "$source_path" "$target_path"
    echo "Installed into '$target_path'"
}

install_script ConsoleControlSurface
