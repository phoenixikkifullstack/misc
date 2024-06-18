#!/bin/bash

info() {
    # 32 green
    ARGE=$1
    echo -e "\033[32mINFO: $ARGE\033[0m"
    #echo -e "\033[0m"
}

alarm() {
    # 35 purple
    ARGE=$1
    echo -e "\033[35mINFO: $ARGE\033[0m"
    #echo -e "\033[0m"
}

warning() {
    # 31 red
    ARGE=$1
    echo -e "\033[31mINFO: $ARGE\033[0m"
    #echo -e "\033[0m"
}

func_main() {
    info    "log-level: <info>"
    alarm   "log-level: <alarm>"
    warning "log-level: <warning>"
}

## main process
func_main