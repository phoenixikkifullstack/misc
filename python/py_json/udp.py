#!/usr/bin/python


from socket import *
from time import *

g_send_count = 0;

def udp_client():
    udp_client_socket = socket(AF_INET, SOCK_DGRAM);

    server_addr = ('172.16.130.97', 60000);

    #udp_client_socket.connect((server_ip, server_port));

    send_data = "hello world...hello world...hello world...hello world...";

    global g_send_count;
    #udp_client_socket.send(send_data.encode("gbk"));
    while True:
        udp_client_socket.sendto(send_data.encode(), server_addr);
        g_send_count += 1;
        '''
        if g_send_count % 5000 == 0:
            print("Have a nap...")
            sleep(0.1)
        '''
        if g_send_count >= 100000:
            break;

    print("Total msg send:{}".format(g_send_count));
    '''
    #recvData = udp_client_socket.recv(1024);
    recvData = udp_client_socket.recv(1024);
    print('resp type:[{}]'.format(type(recvData)));
    print('recv data:'+ recvData.decode());
    '''

    udp_client_socket.close();

if __name__ == '__main__':
    udp_client();
    pass;
