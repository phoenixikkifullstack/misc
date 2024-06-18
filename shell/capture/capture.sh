#!/bin/bash

## loop capture with pcap file rorate

NIC_NAME=enp11s0f0
CURRENT_DAY=`date +%Y%m%d`
TARGET_DIR=/tmp/${CURRENT_DAY}


mkdir -p ${TARGET_DIR}

echo "==>>Captures will be saved in ${TARGET_DIR}<<=="

# 10Mb/file, counts 50
tcpdump -i ${NIC_NAME} -vnnp -C 10 -Z root -W 50 -w ${TARGET_DIR}/rawpkt.pcap
