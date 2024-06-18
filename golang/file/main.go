package main

import (
    "fmt"
    "os"
    "io"
    "bufio"
)

var file_eve string = "./eve.json"

func main() {
    f, err := os.Open(file_eve)
    if err != nil {
        panic(err)
    }
    defer f.Close()

    n := 0
    rd := bufio.NewReader(f)
    for {
        line, err := rd.ReadString('\n')
        if err != nil || err == io.EOF {
            if line=="" {
                fmt.Println("line...")
                break
            }
        }
        n++
        // fmt.Println(line)
    }
    fmt.Printf("[==>>]n:%v\n", n)
    return
}
