#!/bin/bash

if [ -f ./.local/results.json ]; then
    rm ./.local/results.json
fi

for i in {1..6}; do
    echo "Running simulation for scene $i"
    uv run ./main.py simulate "$i" --restore
done
