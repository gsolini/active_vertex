#!/bin/bash

((N = "$1"*"$1"*"$1"))


for i in $(seq 0 $(($N-1)))
do
    sbatch run_analysis.sh "$i" "$1" "$2"
done