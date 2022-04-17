#!/bin/bash
for s in $@
do
    python update.py -s $s
    git add data/$s/*.json
    git commit -m "update data/$s" || echo nothing to commit
done