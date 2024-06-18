#!/bin/bash

NFT_RULES=/usr/local/ips/rules.nft

if [ $# -lt 1 ]; then
	echo "At least one more params..."
	exit 1
fi

if [ "$1" = "load" ]; then
	echo "load rules"
	## 1. set nft rules
	nft -f /usr/local/ips/rules.nft

	## 2. set ipt rules
	/bin/bash /usr/local/ips/ipt.sh
elif [ "$1" = "flush" ]; then
	echo "flush rules"
	nft flush ruleset
	iptables -F
fi
