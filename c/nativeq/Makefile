sources = $(wildcard *.c)

#OBJS = $(patsubst %.c,%.o,$(sources))
OBJS =  main.o
target = main

CC = gcc
INCLUDES = -I.
CFLAGS = -Wall -g
LDFLAGS = -lpthread -lrt

$(target):$(OBJS)
	$(CC) -o $@ $^ $(LDFLAGS) -Wl,-rpath=. -L.

.c.o:
	@#$(CC) -c -fPIC -o $@ $< $(CFLAGS) $(INCLUDES)
	$(CC) -c -fPIC $(CFLAGS) $(INCLUDES) -o $@ $<

clean:
	rm -rf $(target) $(OBJS)

.PHONY: all clean
