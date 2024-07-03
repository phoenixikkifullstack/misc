sources = $(wildcard *.c)

#OBJS = $(patsubst %.c,%.o,$(sources))
OBJS =  async_queue.o
MAIN_OBJ = main.o

CC = gcc
INCLUDES = -I.
CFLAGS = -Wall -g
LDFLAGS = -lpthread -lrt

target_d = libaqueue.so
# target_s = libmap.a
target_m = main

# all: $(target_d) $(target_s) $(target_m)
all: $(target_d) $(target_m)

$(target_d):$(OBJS)
	$(CC) -shared -o $@ $^ $(LDFLAGS)

#$(target_s):$(OBJS)
#	ar rc $@ $?
#	ranlib $@

$(target_m):$(MAIN_OBJ)
	$(CC) -o $@ $^ $(LDFLAGS) -Wl,-rpath=. -L. -laqueue

.c.o:
	@#$(CC) -c -fPIC -o $@ $< $(CFLAGS) $(INCLUDES)
	$(CC) -c -fPIC $(CFLAGS) $(INCLUDES) -o $@ $<

install:
	cp -d $(target_d) $(PREFIX)
	@#cp -d $(target_s) $(PREFIX)
	cp -d *.h $(PREFIX)

clean:
	@#rm -rf $(target_d) $(target_s) $(target_m) $(OBJS) $(MAIN_OBJ)
	rm -rf $(target_d) $(target_m) $(OBJS) $(MAIN_OBJ)

.PHONY: all install clean
