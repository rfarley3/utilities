#!/usr/bin/env bash

len=`curl -sI $1 | awk '/[Cc]ontent-[Ll]ength/ { print $2 }' | tr -d '\r' | tr -d '\n'`
kbytes=$((len / 1024))
mbytes=$((kbytes / 1024))
# echo "${len}B ${kbytes}KB ${mbytes}MB"

# mac=`curl -sI $1 | awk '/[Ll]ast-[Mm]odified/ { for (i=2; i<NF; i++) print $i " " }' | tr -d '\r' | tr -d '\n'`
mac=`curl -sI $1 | grep -i 'Last-Modified' | cut -d' ' -f 2- | tr -d '\r' | tr -d '\n'`
# mac=`curl -sI $1 | grep -i 'Last-Modified' | tr -d '\r' | tr -d '\n'`

printf "Size:\t\t%'dB (%'dKB, %'dMB)\n" $len $kbytes $mbytes
echo "Last modified: " $mac

