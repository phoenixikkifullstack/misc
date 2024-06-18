TARGET_S = udpserver
TARGET_C = udpclient

all:
	go build -x -o=./udpserver server/server.go
	go build -x -o=./udpclient client/client.go

clean:
	go clean
	rm $(TARGET_S) $(TARGET_C)

