package main

import (
    "fmt"
    _ "time"
    u "unixsocket"
)

const (
    socket_addr = "./us.sock"
)

func main() {
    //声明unixsocket
    us := u.NewUnixSocket(socket_addr)
    //发送数据unixsocket并返回服务端处理结果
    r := us.ClientSendContext("hello world")
    fmt.Println(">>>>>>"+ r)
}
