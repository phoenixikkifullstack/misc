sources = $(wildcard *.c)

OBJS = $(patsubst %.c,%.o,$(sources))

target = main

all: $(target)

LD_FLAGS=-lnetfilter_queue
INCLUDES=/usr/local/include

$(target):$(OBJS)
	@gcc -o $@ $^ $(LD_FLAGS)
	@echo "CCLD    $@"

.c.o:
	@gcc -c -o $@ $< -I $(INCLUDES)
	@echo "CC    $@"

clean:
	rm -rf main main.o

.PHONY: all clean
