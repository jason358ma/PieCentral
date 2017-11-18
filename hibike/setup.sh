#!/bin/bash

if ! command -v pipenv &> /dev/null; then
    pip3 install pipenv
fi
pip3 install setuptools

version=""
if [ "$1" != "" ]; then
    case $1 in
        --version )
            version="--python $2"
            ;;
    esac
fi

pipenv install $version --dev
sudo ./sudo_setup.sh
echo "All dependencies installed."
