#!/usr/bin/env bash

file=$1

tot=$( grep -c '.txt' $file )
suc=$( grep -c True $file )
fal=$( grep -c False $file )

suc_pc=$( echo "scale=2; 100 * $suc / $tot" | bc )
echo "$suc_pc%"
