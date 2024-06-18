#!/bin/bash

## TODO
iptables -I INPUT -p tcp --dport 0:65535 -j DROP
iptables -I INPUT -s 192.168.99.1 -p tcp --dport 0:65535 -j ACCEPT
iptables -I INPUT -s 192.168.99.3 -p tcp --dport 0:65535 -j ACCEPT
iptables -I INPUT -s 127.0.0.1/8 -p tcp --dport 0:65535 -j ACCEPT
iptables -I INPUT -p udp --dport 0:65535 -j DROP
iptables -I INPUT -s 192.168.99.1 -p udp --dport 0:65535 -j ACCEPT
iptables -I INPUT -s 192.168.99.3 -p udp --dport 0:65535 -j ACCEPT
iptables -I INPUT -s 127.0.0.1/8 -p udp --dport 0:65535 -j ACCEPT