sources = $(wildcard *.py)

all:
	python -m py_compile $(sources)
	gcc -o c_udp c_udp.c
	gcc -o server_c server_c.c -lpthread

clean:
	rm -rf *.pyc c_udp

.PHONY: all clean

