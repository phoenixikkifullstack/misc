#include <stdio.h>
#include <pcap.h>
#include <libnet.h>

int main(int argc, char *argv[]) {
    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t *pcap;
    const u_char *packet;
    struct pcap_pkthdr header;
    libnet_t *l;
    uint32_t count = 0;
    
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <Device> <Pcap File>\n", argv[0]);
        exit(1);
    }

    // 打开网络设备
    l = libnet_init(LIBNET_LINK_ADV, argv[1], errbuf);
    if (l == NULL) {
        fprintf(stderr, "libnet_init() failed: %s\n", errbuf);
        exit(EXIT_FAILURE);
    }

    // 打开pcap文件
    pcap = pcap_open_offline(argv[2], errbuf);
    if (pcap == NULL) {
        fprintf(stderr, "Couldn't open pcap file %s: %s\n", argv[1], errbuf);
        libnet_destroy(l);
        return(2);
    }

    fprintf(stderr, "[***]PCAP_FILE[%s] ====>>> NIC[%s]\n", argv[2], argv[1]);

    // 从pcap文件中读取并发送数据包
    while ((packet = pcap_next(pcap, &header)) != NULL) {
        if (libnet_write_link(l, (u_int8_t *)packet, header.len) == -1) {
            fprintf(stderr, "libnet_write_link() failed: %s\n", libnet_geterror(l));
        }
        count++;
    }

    // 关闭网络设备和pcap文件
    libnet_destroy(l);
    pcap_close(pcap);

    printf("[***]Finished, [%u] pkts be send\n", count);

    return 0;
}
