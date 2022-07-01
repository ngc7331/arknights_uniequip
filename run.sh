#!/bin/bash
for s in $@
do
    echo "=== updating $s ==="
    echo "-> run script"
    python update.py -s $s
    ret=$?
    if [ $ret -ne 0 ]; then
        echo "python run failed with exit code $ret"
        continue
    fi
    echo "-> commit"
    git add data/$s/*.json
    git commit -m "update data/$s" && echo "..done" || echo "..nothing to commit"
done