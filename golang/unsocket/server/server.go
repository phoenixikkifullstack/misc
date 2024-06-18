package main

import (
    "fmt"
    _"os"
    "time"
    u "unixsocket"
)

const (
    socket_addr = "./us.sock"
)

func main() {
    //声明unixsocket
    us := u.NewUnixSocket(socket_addr)
    //设置服务端接收处理
    us.SetContextHandler(func(context string) string {
        fmt.Println(context)
        now := time.Now().String() + "<<<<<<"
        return now
    })
    //开始服务
    us.StartServer()
    /*
    go us.StartServer()
    time.Sleep(time.Second * 30)
    */
}
