#!/bin/sh

#enable legacy boot
#sudo crossystem dev_boot_usb=1 dev_boot_legacy=1

#flash firmware
#cd; curl -LO https://mrchromebox.tech/firmware-util.sh && sudo bash firmware-#util.sh

# Get Latest Dawn Version URL
PYTHON_CMD="import json, sys"
PYTHON_CMD="$PYTHON_CMD; assets = json.loads(sys.stdin.read())['assets']"
PYTHON_CMD="$PYTHON_CMD; print([asset['browser_download_url'] for asset in assets if asset['name'].startswith('dawn-linux-x64')][0])"
DAWN_URL=$(curl https://api.github.com/repos/pioneers/PieCentral/releases/latest | python -c "$PYTHON_CMD")

# Download Dawn to /tmp
wget -O /tmp/dawn.zip $DAWN_URL

# Unzip dawn.zip to Desktop, replace if same name exist
cd /tmp
unzip -o dawn.zip -d ~/D

# Remove /tmp/dawn.zip
rm -rf /tmp/dawn.zip

# install vim & git
sudo apt install --yes vim git

# clone the git(perminant) and run the setup.sh, then do the change
cd
cd Desktop
git clone https://github.com/pioneers/PieCentral.git

cd PieCentral/hibike

# Specify Python version to 3.5
./setup.sh --version 3.5
