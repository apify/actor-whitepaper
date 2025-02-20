#!/bin/bash

echo "󰋼  Starting sync test..."

WORK_DIR="test-sync"
rm -rf $WORK_DIR
echo -e "\n󰋼  Creating work directory: $WORK_DIR"
mkdir -p $WORK_DIR
cd $WORK_DIR

echo -e "\n"

if [ ! -d "source" ]; then
    echo -e "\n󰋼  Copying source files..."
    mkdir source
    cp -r ../{img,pages,*.md,requirements.txt,scripts} source/
    echo -e "\n  Source files copied"
else
    echo -e "\n󰋼  Using existing source directory"
fi

echo -e "\n"

if [ ! -d "target" ]; then
    echo -e "\n󰋼  Cloning target repository..."
    git clone https://github.com/apify/actor-whitepaper-web target
    git checkout feat/gh-57-content-sync # REMOVE THIS LINE
    echo -e "\n  Target repository cloned"
else
    echo -e "\n󰋼  Using existing target directory"
fi

echo -e "\n"

echo -e "\n󰋼  Updating target repository..."
cd target
git pull origin main
cd ..

echo -e "\n"

echo -e "\n󰋼  Setting up Python virtual environment..."
cd source
pwd

if [ ! -d "../.venv" ]; then
    echo -e "\n󰋼  Setting up Python virtual environment..."
    cd ..
    python3 -m venv .venv
    cd -
fi

source ../.venv/bin/activate || source ../.venv/Scripts/activate

echo -e "\n"

echo -e "\n󰋼  Installing Python dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install -r ./requirements.txt

echo -e "\n"
echo -e "\n󰋼  Running MD to MDX conversion..."
cd ..
python3 source/scripts/md2mdx.py
cd source

echo -e "\n"

echo -e "\n󰋼  Checking changes in target repository..."
cd ../target
git status

echo -e "\n"

echo -e "\n  Check changes in ${WORK_DIR}/target"

deactivate

echo -e "\n󰋼  Done"
