TARGET_S = unserver
TARGET_C = unclient

all:
	#go build -x -o=./unserver server/server.go
	#go build -x -o=./unclient client/client.go
	go build -o=./unserver server/server.go
	go build -o=./unclient client/client.go

clean:
	go clean
	rm $(TARGET_S) $(TARGET_C)

