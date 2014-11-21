#! /bin/sh
#######################################
# Nov 2014 rfarley3
# wrapper for fgrep, mostly controls --includes
# change INCLUDES to match your source type

if [ $# -eq 0 ] || [ $# -gt 2 ] ; then
	echo "Search a directory for strings within source files"
	echo "\t$0 <pattern>  will search from the current directory"
	echo "\t$0 <file|dir> <pattern>"
	exit
fi

FILE="./"
PATTERN="$1"
if [ $# -eq 2 ] ; then
	FILE="$1"
	PATTERN="$2"
fi

INCL_PY="--include *.py"
INCL_C="--include *.c --include *.h"
INCL_CPP="--include *.cpp --include *.hpp"
INCL_FL="--include *.flex"
INCLUDES="${INCL_PY} ${INCL_C} ${INCL_CPP} ${INCL_FL}"

echo "----------------------------------------------------"
echo "file|dir: ${FILE}"
echo "pattern : ${PATTERN}"
echo "includes: ${INCLUDES}"
echo "----------------------------------------------------"

# search contents, for pattern, of files with names that match includes
# -R              recursive
# --color=always  output color escapes, regardless of the fact it detects a pipe
# -n              makes it show line numbers
# 2> /dev/null    discard all stderr
# sed ...         make output cleaner by getting rid of root dir (note, rem if you want to see full paths)
grep -n --color=always -R ${INCLUDES} "${PATTERN}" ${FILE} 2> /dev/null | sed -e "s|${FILE}/||" 

# TODO
# work output st you show filename once
# then each line has setw line number and that line's output

