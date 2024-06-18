sources = $(wildcard *.c)

OBJS = $(patsubst %.c,%.o,$(sources))

CC = gcc
INCLUDES = -I./
CFLAGS = -Wall -g
LDFLAGS = -lpthread

target = main

all: $(target)

$(target):$(OBJS)
	$(CC) -o $@ $^ $(LDFLAGS)

.c.o:
	$(CC) -c -o $@ $< $(CFLAGS) $(INCLUDES)

clean:
	rm -rf $(target) $(OBJS)

.PHONY: all clean
