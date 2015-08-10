#!/bin/sh
#######################################
# Nov 2014 rfarley3
# wrapper for fgrep, mostly controls --includes
# change INCLUDES to match your source type

if [ $# -eq 0 ] || [ $# -gt 3 ] ; then
	echo "Search a directory for strings within source files"
	echo "\t$0 <pattern>  will search from the current directory"
	echo "\t$0 <file|dir> <pattern>"
	echo "\t$0 <file|dir> <pattern> -i  # to make case insensitive"
	exit
fi

FILE="./"
PATTERN="$1"
CASE=""
if [ $# -gt 1 ] ; then
	FILE="$1"
	PATTERN="$2"
fi
if [ $# -gt 2 ] ; then
	CASE="-i"
fi

echo "----------------------------------------------------"
echo "file|dir: ${FILE}"
echo "pattern : ${PATTERN}"

# search contents, for pattern, of files with names that match includes
# -n              makes it show line numbers
# --color=always  output color escapes, 
#                 regardless of the fact it detects a pipe
# -s              don't show output about files it didn't process
# -R              recursive
# -E              interpret pattern as regex (like egrep)
# 2> /dev/null    discard all stderr
# sed ...         make output cleaner by getting rid of root dir 
#                 (note, rem if you want to see full paths)
CMD="grep -n --color=always --binary-files=without-match -s -R --exclude-dir .git ${CASE} -E \"${PATTERN}\" ${FILE} 2> /dev/null"
CMD="${CMD} | sed -e 's|${FILE}||' | sed -e 's|^/||'"
echo "running : ${CMD}"
echo "----------------------------------------------------"
eval ${CMD}

# TODO
# work output st you show filename once
# then each line has setw line number and that line's output

