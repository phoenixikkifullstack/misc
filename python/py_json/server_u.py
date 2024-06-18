#!/usr/bin/python


from socket import *
import time

#server_addr = ('127.0.0.1', 60000);
server_addr = ('172.16.130.97', 60000);
server_socket = socket(AF_INET, SOCK_DGRAM);
server_socket.bind(server_addr);
server_socket.settimeout(10);

g_msg_count = 0;

while True:
    try:
        now = time.time();
        recv_data, client = server_socket.recvfrom(1024);
        #print('------------------------------------------------------');
        #print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now)));
        #print('------------------------------------------------------');
        g_msg_count = g_msg_count + 1;
        #print("g_count:[%d], recv from[%s], data[%s]" % (g_msg_count, client, recv_data));
        #print('------------------------------------------------------');
        #server_socket.sendto("Copy that...", client)
    except:
        print("time out[10s], last recv total counts:{}".format(g_msg_count))
        #print("time out[10]...");
        g_msg_count = 0;
        #pass;

