#!/bin/bash

cwd=`pwd`
ips_dir=/usr/local/ips
systemd=/etc/systemd/system

func_install() {
	echo "Install ips.service"
	install -c -d ${ips_dir}
	cp -fr ${cwd}/ips.service ${systemd}
	cp -fr ${cwd}/rules.nft ${ips_dir}
	cp -fr ${cwd}/ips.sh ${ips_dir}
	cp -fr ${cwd}/ipt.sh ${ips_dir}

	## set enable
	systemctl enable ips.service
}

if [ $# -lt 1 ]; then
	#echo "At least one more params"
	echo "Usage: ./config.sh install"
	exit 1
fi

if [ "$1" = "install" ]; then
	func_install
fi
