sources = $(wildcard *.cpp)

OBJS = $(patsubst %.cpp,%.o,$(sources))

CC = g++
INCLUDES = -I./
CFLAGS = -std=c++11 -Wall -g
LDFLAGS = -lpthread

target = main

all: $(target)

$(target):$(OBJS)
	$(CC) -o $@ $^ $(LDFLAGS)

.cpp.o:
	$(CC) -c -o $@ $< $(CFLAGS) $(INCLUDES)

clean:
	rm -rf $(target) $(OBJS)

.PHONY: all clean
