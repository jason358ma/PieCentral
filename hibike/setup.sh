#!/bin/bash

if ! command -v pipenv &> /dev/null; then
    pip3 install pipenv
fi

version=""
while ["$1" != ""]; do
    case $1 in
        --version)
            version="--python $2"
            exit;
    esac
done

pipenv --dev $version install

sudo ./sudo_setup.sh

echo "All dependencies installed."
