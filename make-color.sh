#!/bin/bash -e
#######################################
# rfarley3
# make-color.sh
#
# README
#    * a wrapper for make so you get to see colored output
#    * useful if your gcc doesn't support this
#
# COLORS
#   Your colors may be different than mine, I use zenburn, which makes the yellow dull and non-bold red gray.
#   https://ask.fedoraproject.org/en/question/7000/how-to-set-colors-for-bash-shell-primary-prompt/
#
#   Important events are in green (entire line)
#   Compiling is in green (just the compiler executable name)
#   Linking is in blue (entire line)
#
#   Warnings are yellow (entire line)
#   Compiler/linker errors are red underlined
#   Make errors are bold red; and cause this program to exit
#
# METHODOLOGY
#    Calls make, pushing stderr over stdout, piping all into a perl parser
#    For each line read perl does a conditional OR, allowing it to exit at the first match
#    If the line matches a regex, then it is a color code, the line, and a color clearing code is printed
#    Codes are injected via regex replace or print, depending on if you want to color entire line or segment
#    If it matches Error, then it also exits
#    If nothing matches, it prints clear . line . clear
#
# INSTALL
#    * requires perl
#    * put somewhere in your path
#    * set up an alias in your .profile or .bash_rc: alias make='make-color.sh'
#########################################

make ${@} 2>&1 | perl -wln -M'Term::ANSIColor' -e '
m/Entering directory|Leaving directory|Building|CXX/i and print "\e[1;32m", "$_", "\e[0m"
or 
s/(gcc|g\+\+)/\e\[1\;32m$1\e\[0m/ and print "$_" 
or
m/Error/ and print "\e[1;91m", "$_", "\e[0m" and exit (1)
or
s/(\s)error([^s\.-])/$1\e\[4\;31merror\e\[0m$2/ and print "$_"
or
m/Warning/i and print "\e[0;93m", "$_", "\e[0m"
or
m/Linking|\.a\b|[\s](AR|LD)[\s]/i and print "\e[0;36m", "$_", "\e[0m"
or
print "\e[0m", "$_", "\e[0m";'

