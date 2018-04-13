#!/bin/bash

echo "Start"
mkdir -p ../test/log
for i in {0..29}; do
    if [ $i -lt 10 ] 2>/dev/null; then
        echo "start" > ../test/log/r$i.log
    elif [ $i -lt 20 ] && [ $i -gt 9 ] 2>/dev/null; then
        echo "start" > ../test/log/g$((i-10)).log
    else
        echo "start" > ../test/log/z$((i-20)).log
    fi
done

filename="base.txt"
while read -r line
do
    name="$line"
    echo "Name read from file - $name"
    for entry in "$search_dir"../test/log/*
    do
      #echo "$entry"
      sleep 0.1 && echo "$name" >> "$entry"
    done


done < "$filename"







