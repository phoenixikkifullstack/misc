package main

/*
 * Auto Generate by ChatGPT-3.5
 */
import (
    "fmt"
    "io"
    "net"
)

func handleClient(clientConn net.Conn, targetAddr string) {
    // 连接目标服务器
    targetConn, err := net.Dial("tcp", targetAddr)
    if err != nil {
        fmt.Println("Error connecting to target server:", err)
        clientConn.Close()
        return
    }
    defer targetConn.Close()

    // 启动一个goroutine将目标服务器的响应返回给客户端
    go func() {
        io.Copy(clientConn, targetConn)
        clientConn.Close()
    }()

    // 将客户端的请求转发到目标服务器
    io.Copy(targetConn, clientConn)
}

func main() {
    // 代理监听地址和端口
    listenAddr := "127.0.0.1:10000"
    // 目标服务器地址和端口
    targetAddr := "127.0.0.1:8080"

    // 监听代理地址
    listener, err := net.Listen("tcp", listenAddr)
    if err != nil {
        fmt.Println("Error listening:", err)
        return
    }
    defer listener.Close()

    // ==>> listenAddr <<==>> targetAddr
    fmt.Printf("Proxy is listening on %s and forwarding to %s\n", listenAddr, targetAddr)

    for {
        // 等待客户端连接
        clientConn, err := listener.Accept()
        if err != nil {
            fmt.Println("Error accepting connection:", err)
            continue
        }

        // 启动一个goroutine处理客户端请求
        go handleClient(clientConn, targetAddr)
    }
}
