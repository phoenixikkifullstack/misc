sources = $(wildcard *.c)

OBJS = $(patsubst %.c,%.o,$(sources))

target 	= pcap_send
target1 = pcap_send1

all: $(target) $(target1)

LD_FLAGS=-lpcap -lnet
INCLUDES=/usr/local/include

$(target) : pcap_send.o
	@gcc -o $@ $^ $(LD_FLAGS)
	@echo "CCLD    $@"

$(target1) : pcap_send1.o
	@gcc -o $@ $^ $(LD_FLAGS)
	@echo "CCLD    $@"

.c.o:
	@gcc -c -o $@ $< -I $(INCLUDES)
	@echo "CC    $@"

clean:
	rm -rf $(target) $(target1) $(OBJS)

.PHONY: all clean
