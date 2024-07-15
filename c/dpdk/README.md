## 1. dpdk-build
```bash
cd dpdk-stable-20.11.10/
/root/dpdk-stable-20.11.10
export DPDK_BUILD=$(pwd)/build
apt install meson ninja-build
apt install build-essential
apt install libbpf-dev

meson build
ninja -C build
ninja -C build install
ldconfig
pkg-config --modversion libdpdk
pkg-config --cflags libdpdk
pkg-config --libs libdpdk
# /usr/local/include/
# /usr/local/lib/x86_64-linux-gnu/

## HUGE-PAGES
echo 1024 > /sys/devices/system/node/node0/hugepages/hugepages-2048kB/nr_hugepages

##Q&A
### Q1: Warning: routing table indicates that interface 0000:02:05.0 is active. Not modifying
### A1: ip link set dev down

### Q2: root@ubuntu:~/dpdk-stable-20.11.10/usertools# ./dpdk-devbind.py -b vfio-pci 0000:02:05.0
###  Error: bind failed for 0000:02:05.0 - Cannot bind to driver vfio-pci
### A2: You have to enable unsafe mode to bind via VFIO-pci if there is no IOMMU available on the system, VFIO can still be used, but it has to be loaded with an additional module parameter:
###     modprobe vfio enable_unsafe_noiommu_mode=1
### OR  echo 1 > /sys/module/vfio/parameters/enable_unsafe_noiommu_mode

```
## 2. suricata 7.0.6
```bash
## compile-toolkits
apt -y install autoconf automake build-essential cargo \
    libjansson-dev libpcap-dev libpcre2-dev libtool \
    libyaml-dev make pkg-config rustc zlib1g-dev \
    libnetfilter-queue-dev libnuma-dev
## source code
wget https://www.openinfosecfoundation.org/download/suricata-7.0.6.tar.gz
tar zxf suricata-7.0.6.tar.gz
cd suricata-7.0.6
./configure --enable-nfqueue --enable-dpdk --prefix=/opt/suricata706
make
## error: conflicting types for ‘AppLayerTxData’; have ‘struct <anonymous>’
# cargo install --force cbindgen
##      3.1.2.4. Rust support
##      Rust packages can be found in package managers but some distributions don't provide Rust or provide outdated Rust packages. In case of insufficient version you can install Rust directly from the Rust project itself:
##
##      1) Install Rust https://www.rust-lang.org/en-US/install.html
##      2) Install cbindgen - if the cbindgen is not found in the repository
##      or the cbindgen version is lower than required, it can be
##      alternatively installed as: cargo install --force cbindgen
##      3) Make sure the cargo path is within your PATH environment
##      echo 'export PATH="~/.cargo/bin:${PATH}"' >> ~/.bashrc
##      export PATH="~/.cargo/bin:${PATH}"

make install

mkdir -p /opt/suricata706/var/log/suricata
mkdir -p /opt/suricata706/var/run/suricata
cp suricata.yaml /opt/suricata706/

## run in nfq
/opt/suricata706/bin/suricata -c /opt/suricata706/suricata.yaml -q 0

## run in dpdk
/opt/suricata706/bin/suricata -c /opt/suricata706/suricata.yaml --dpdk

## 3. test with vmware workstation
[ pcapreplay in windows ] ==> [ vmnetwork1 ] ==> [ capture in linux ]

```
