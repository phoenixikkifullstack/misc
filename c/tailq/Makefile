sources = $(wildcard *.c)

OBJS = $(patsubst %.c,%.o,$(sources))

CC=g++ -std=c++11

target 	= main

all: $(target)

LD_FLAGS=
INCLUDES=/usr/local/include

$(target) : $(OBJS)
	$(CC) -o $@ $^ $(LD_FLAGS)
	@#echo "CCLD    $@"

.c.o:
	$(CC) -c -o $@ $< -I $(INCLUDES)
	@#echo "CC    $@"

clean:
	rm -rf $(target) $(OBJS)

.PHONY: all clean
