#!/bin/bash

WORK_DIR="sync"

echo "󰋼  Starting sync test..."

rm -rf $WORK_DIR
mkdir -p $WORK_DIR
cd $WORK_DIR

if [ ! -d "source" ]; then
    mkdir source
    cp -r ../{pages,*.md} source/
    echo -e "\n  Source files copied"
else
    echo -e "\n󰋼  Using existing source directory"
fi

echo -e "\n\n"

if [ ! -d "target" ]; then
    git clone https://github.com/apify/actor-whitepaper-web target
    echo -e "\n  Target repository cloned"
else
    echo -e "\n󰋼  Using existing target directory"
fi

echo -e "\n\n"

cd target
git pull origin main
echo -e "\n  Target repository updated"

echo -e "\n\n"

cd ../..

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo -e "\n  Python virtual environment created"
fi

echo "Current path: $(pwd)"
source .venv/bin/activate

echo -e "\n\n"

python3 -m pip install --upgrade pip
python3 -m pip install -r ./requirements.txt
echo -e "\n  Python dependencies installed"

echo -e "\n\n"
echo "Current path: $(pwd)"
python3 scripts/md2mdx.py --source $WORK_DIR/source --target $WORK_DIR/target
echo -e "\n  MD to MDX conversion completed"

echo -e "\n\n"

cd target
git status
echo -e "\n  Target repository status checked"
cd ..

echo -e "\n\n"

echo -e "\n  Check changes in ${WORK_DIR}/target"

deactivate

echo -e "\n󰋼  Done"
