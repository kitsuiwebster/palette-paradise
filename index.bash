#!/bin/bash

echo "👉 rename_raws.py"
python3 rename_raws.py
echo "👉 crop.py"
python3 crop.py
echo "👉 git add"
git add .
echo "👉 git commit"
git commit -m "feat: update workflow"
echo "👉 git puush"
git puush

