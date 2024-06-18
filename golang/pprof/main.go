package main

import (
    "time"
    "log"
    // "runtime"
    "net/http"
    _ "net/http/pprof"
)

func main() {
    /*
     * 1. compile & run current main program,
     *      $ go run main.go
     * 2. browser the web http://localhost:9527/debug/pprof/profile
     * 3. type in local bash,
     *      $ go tool pprof http://localhost:9527/debug/pprof/profile
    */
    go func() {
        http.ListenAndServe("127.0.0.1:9527", nil)
    } ()

    var i uint64 = 0
    for {
        time.Sleep(2 * time.Second)
        // runtime.GC()
        log.Println("[==>>] loop index:", i)
        i++
    }
}