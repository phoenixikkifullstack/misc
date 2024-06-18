package main

import (
    "os"
    "io"
    "fmt"
    "bufio"
    _"bytes"
)

func main() {
    file, err := os.Open("./opc.log")
    if err != nil {
        err1 := fmt.Errorf("%v", err)
        fmt.Println(err1)
        os.Exit(-1)
    }
    defer file.Close()

    var size int
    reader := bufio.NewReader(file)

    for {
        // line, err := reader.ReadString('\n')
        lineb, err := reader.ReadBytes('\n')
        if err != nil {
            if io.EOF == err {
                // fmt.Printf("file size:[%d]", size)
                fmt.Print(string(lineb))
                size += len(lineb)
                break
            } else {
                fmt.Println("error:", err)
                os.Exit(-1)
            }
        }
        // fmt.Print(line)
        // size += len(line)
        fmt.Print(string(lineb))
        size += len(lineb)
    }

}