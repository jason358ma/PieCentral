#!/bin/sh

#enable legacy boot
#sudo crossystem dev_boot_usb=1 dev_boot_legacy=1

#flash firmware
#cd; curl -LO https://mrchromebox.tech/firmware-util.sh && sudo bash firmware-#util.sh

# Download Dawn
if [ ! -d ~/Desktop/dawn-linux-x64 ]; then
  # Get URL of latest Dawn
  PYTHON_CMD="import json, sys"
  PYTHON_CMD="$PYTHON_CMD; assets = json.loads(sys.stdin.read())['assets']"
  PYTHON_CMD="$PYTHON_CMD; print([asset['browser_download_url'] for asset in assets if asset['name'].startswith('dawn-linux-x64')][0])"
  DAWN_URL=$(curl https://api.github.com/repos/pioneers/PieCentral/releases/latest | python -c "$PYTHON_CMD")

  wget -O /tmp/dawn.zip $DAWN_URL
  unzip -o /tmp/dawn.zip -d ~/Desktop

  rm /tmp/dawn.zip
fi

sudo apt install -y vim git

# Install Hibike dependencies
cd ~/Desktop
if [ ! -d PieCentral ]; then
  git clone https://github.com/pioneers/PieCentral.git
fi
cd PieCentral/hibike
./setup.sh --version 3.5
