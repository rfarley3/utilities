#!/bin/sh
##################################
# Oct 2014 rfarley3
# search the current directory for any 
# files that contain DOS line endings (CLRF)

# -I ignore bin files
# -l list name only (not lines)
# -s silent mode, suppress error output
# -r or -R recursive
# -n line number
grep -RIls $'\r$' .   # yet another & even shorter alternative

