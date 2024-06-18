# 单台虚拟机实现ingress hook点抓包

在同一台机器上，将数据包直接发送至网卡时，数据包不经过ingress点。导致在开发调试时，缺少模拟环境，开发人员无法及时排查与修改问题。

通过虚拟网卡对veth-pair，对其中一张网卡veth0发包，在另一张veth1网卡hook ingress，即可以实现ingress的抓包。

## 1. 创建veth-pair虚拟网卡对
```bash
ip link add dev veth0 type veth peer name veth1
ip link set dev veth0 up
ip link set dev veth1 up
```

## 2. 在新namespace配置nft规则，并启动引擎
### 2.1 nft规则
```bash
table netdev netdev-netvine-table {
    chain base-rule-chain-ens37 {
        type filter hook ingress device "veth1" priority filter; policy drop;
         #counter meta mark set 9527 queue num 0 bypass
         # counter th dport 502 counter queue num 0-3 bypass
         counter queue num 0 bypass
         # counter
         # counter accept
    }
}
```

### 2.2 加载规则
```bash
nft list ruleset
nft flush ruleset
nft -f ${WORK_DIR}/rule.nft
```

### 2.3 引擎启动
```bash
.lib/netvine_engine -c netvine_engine/netvine_engine.yaml -q 0
```

## 3. 模拟报文发送至veth0，在veth1即可收到包，抓包验证
```bash
tcpdump -i veth1
```

## 4. 发包程序demo
### 4.1 code
```bash
// pcap_send1.c
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
```

### 4.2 编译
```bash
gcc -o pcap_send1 pcap_send1.c -lpcap -lnet
```

### 4.3 使用
```bash
./pcap_send1 <Device> <Pcap File>
## eg.
## ./pcap_send1 veth0 /root/work/pcap/modbus_503_1.pcap
```
