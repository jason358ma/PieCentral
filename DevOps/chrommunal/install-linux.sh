#!/bin/sh

#enable legacy boot
sudo crossystem dev_boot_usb=1 dev_boot_legacy=1

#flash firmware
cd; curl -LO https://mrchromebox.tech/firmware-util.sh && sudo bash firmware-util.sh

# Get Latest Dawn Version URL
PYTHON_CMD="import json, sys"
PYTHON_CMD="$PYTHON_CMD; assets = json.loads(sys.stdin.read())['assets']"
PYTHON_CMD="$PYTHON_CMD; print([asset['browser_download_url'] for asset in assets if asset['name'].startswitch('dawn-linux-x64')][0])"
DAWN_URL=$(curl https://api.github.com/repos/pioneers/PieCentral/releases/latest | python -c "$PYTHON_CMD")

wget $DAWN_URL -O /tmp/Dawn/dawn.zip

# Unzip dawn.zip to Desktop, replace if same name exist
cd /tmp/Dawn
unzip -o dawn.zip -d ~/Desktop

# Clear /tmp/Dawn
rm -rf /tmp/Dawn/*

# Install Dawn on Desktop

