package main

import (
    "fmt"
    "time"
    "sync"
    "log"
    "channel/mcontex"
)

func main() {
    contex_case()
    // consumer_producer_case()
}

func contex_case() {
    go func() {
        time.Sleep(1*time.Second)
        log.Println("Send_msg==>>")
        mcontex.Send_msg()
    } ()

    log.Println("Waiting for exit msg...")
    mcontex.Wait_msg()
    log.Println("Exiting...")
}

func consumer_producer_case() {
    fmt.Println("hello world...")
    var wg sync.WaitGroup
    var c chan uint64 = make(chan uint64)
    producer(&wg, c)
    consumer(&wg, c)

    wg.Wait()
    // time.Sleep(1* time.Hour)
}

/// producer & consumer  00--begin
func producer(wg *sync.WaitGroup, c chan<- uint64) {
    wg.Add(1)
    go func(wg *sync.WaitGroup) {
        defer wg.Done()
        var i uint64 = 0
        for {
            time.Sleep(1 * time.Second)
            i++
            c <- i
            fmt.Println("Send: [==>>]    i:", i)
        }
    } (wg)
    fmt.Println("Func Producer exit...")
}
func consumer(wg *sync.WaitGroup, c <-chan uint64) {
    wg.Add(1)
    go func(wg *sync.WaitGroup) {
        defer wg.Done()
        for i := range c {
            // i := <- c
            fmt.Println("Recv: [<<==]  i:", i)
        }
    } (wg)
    fmt.Println("Func Consumer exit...")
}
/// producer & consumer  00--end

//// for range/select chan 000--begin
func for_range() {
    fmt.Println("hello world...")

    tk := time.Tick(1 * time.Second)
    for r := range tk {
        fmt.Println(r)
    }
}

func for_select() {
    fmt.Println("hello world...")

    tk := time.Tick(1 * time.Second)
    for {
        select {
            case n := <- tk:
                fmt.Println(n)
        }
    }
}
//// for range/select chan 000--end
