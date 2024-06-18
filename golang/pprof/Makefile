TARGET = pprof

# -m: memory analyse
# -N: debug info
# -l: no inline
# use `go tool compile --help` for more details

all:
	go build -gcflags="-m -N -l" -x -o=$(TARGET) main.go

clean:
	go clean

