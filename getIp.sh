#!/bin/sh
###################################
# To use:
#   set ARGV[1] the interface you want to pull the ip from
#   this should work on any posix (OS X, Linux)
# e.g. ./getip.sh en3
#
###################################

ip=$(ifconfig $1 2>&1 | grep inet | grep -v inet6 | awk '{print $2}')
ip=$(echo $ip | sed s/\s*127.0.0.1\s*//)
if [ "$ip" == "" ]; then
	#echo "Error getting IP, checking if over VPN"
	ip=$(ifconfig utun0 | grep inet | grep -v inet6 | awk '{print $2}')
	if [ "$ip" == "" ]; then
		ip="127.0.0.1"
		#echo "Error getting IP, exiting"
		#exit 1
		# your other option is to connect to remote from local
		# remote machine: ncat -v -t -l 45000
		# local         : ncat -v <ip of remote> 45000
		# on local grep for 'dst <ip> .*'
		# on remote grep for 'Connection from <ip>(.|:).*' 
	fi
fi
echo $ip
