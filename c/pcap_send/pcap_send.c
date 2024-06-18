#include <stdio.h>
#include <pcap.h>
#include <libnet.h>

#define PCAP_FILE   "/root/work/pcap/s7_00.pcap"
#define NIC_NAME_0  "ens37"

#include <stdio.h>
#include <stdlib.h>
#include <pcap.h>

int main(int argc, char *argv[]) {
    pcap_t *handle;
    char errbuf[PCAP_ERRBUF_SIZE];
    struct pcap_pkthdr header;
    const u_char *packet;
    uint32_t count = 0;
    // const char *offline_file = PCAP_FILE;
    // const char *nic = NIC_NAME_0;

    if (argc != 3) {
        fprintf(stderr, "Usage: %s <Device> <Pcap File>\n", argv[0]);
        exit(1);
    }

    fprintf(stderr, "[==>>>]0000 Target NIC [%s]\n", argv[1]);
    // 打开网络设备
    handle = pcap_open_live(argv[1], BUFSIZ, 0, -1, errbuf);
    if (handle == NULL) {
        fprintf(stderr, "Couldn't open device %s: %s\n", argv[1], errbuf);
        exit(1);
    }

    fprintf(stderr, "[==>>>]1111 Pcap FILE[%s]\n", argv[2]);
    // 打开pcap文件
    pcap_t *file_handle = pcap_open_offline(argv[2], errbuf);
    if (file_handle == NULL) {
        fprintf(stderr, "Couldn't open pcap file %s: %s\n", argv[2], errbuf);
        return(2);
    }

    int link_layer_type = pcap_datalink(file_handle);
    
    // 从pcap文件中读取并发送数据包
    while ((packet = pcap_next(file_handle, &header)) != NULL) {
        if (pcap_sendpacket(handle, packet, header.len) != 0) {
            fprintf(stderr, "Error sending packet: %s\n", pcap_geterr(handle));
            return(2);
        }
        count++;
    }

    // 关闭pcap文件和网络设备
    pcap_close(file_handle);
    pcap_close(handle);
    
    printf("Finished, [%u] pkts be send\n", count);

    return 0;
}
