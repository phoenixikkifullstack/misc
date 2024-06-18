#!/bin/sh

set -x
touch test\ 1.txt test\(\).txt
find . -name "test 1.txt" -exec cp {} ./tmp \; >/dev/null 2>&1
#find . -name "test 1.txt" | xargs -i cp {} ./tmp/


