TARGET = channel
all:
	@#go build -x -o=$(TARGET) main.go
	go build -gcflags="-m -N -l" main.go

clean:
	go clean

