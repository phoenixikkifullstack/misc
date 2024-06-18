#!/usr/bin/python

import os

g_json_file = "./eve.json"
#g_json_file = "./test.json"
g_line_count = 0

if __name__ == '__main__':
    f = open(g_json_file, 'rt')
    for line in f:
        g_line_count = g_line_count + 1
        #print(line)

    print("line_count:{}".format(g_line_count))

    f.close()

