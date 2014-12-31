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

#INCL_PY="--include *.py"
#INCL_C="--include *.c --include *.h"
#INCL_CPP="--include *.cpp --include *.hpp"
#INCL_FL="--include *.flex"
#INCL_CONF="--include *.conf --include *.yml"
#INCLUDES="${INCL_PY} ${INCL_C} ${INCL_CPP} ${INCL_FL} ${INCL_CONF}"
#EXCL_PY="--exclude *.pyc"
#EXCL_C="--exclude *.o"
#EXCL_EXE="--exclude *.out --exclude *.exe"
#EXCLUDES="${EXCL_PY} ${EXCL_C} ${EXCL_EXE}"

echo "----------------------------------------------------"
echo "file|dir: ${FILE}"
echo "pattern : ${PATTERN}"
#echo "includes: ${INCLUDES}"
#echo "excludes: ${EXClUDES}"

# search contents, for pattern, of files with names that match includes
# -n              makes it show line numbers
# --color=always  output color escapes, regardless of the fact it detects a pipe
# -s              don't show output about files it didn't process
# -R              recursive
# 2> /dev/null    discard all stderr
# sed ...         make output cleaner by getting rid of root dir (note, rem if you want to see full paths)
CMD="grep -n --color=always --binary-files=without-match -s -R --exclude-dir .git ${EXCLUDES} ${INCLUDES} \"${PATTERN}\" ${FILE} 2> /dev/null"
CMD="${CMD} | sed -e 's|${FILE}||' | sed -e 's|^/||'"
echo "running : ${CMD}"
echo "----------------------------------------------------"
eval ${CMD}

# TODO
# work output st you show filename once
# then each line has setw line number and that line's output

