#!/usr/bin/env bash
##############################################################
# create a proxy friendly tunnel from localhost:$2 to $1:$2
# depends on .bashrc/bash_profile/.profile export proxy=ip:port
# brew install proxytunnel
# ports < 1024 will need sudo
proxytunnel -a $2 -p $proxy -d $1:$2

# usage example:
#   ./tunnel.sh github.com 9418
#   git clone git://localhost/user/repo.git

