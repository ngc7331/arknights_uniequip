#!/bin/bash
for s in $@
do
    python update.py -s $s
    ret=$?
    if [ $ret -ne 0 ]; then
        echo "python run failed with exit code $ret"
        exit $ret
    fi
    git add data/$s/*.json
    git commit -m "update data/$s" || echo nothing to commit
done