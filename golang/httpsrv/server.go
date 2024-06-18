package main

import (
    "fmt"
    "net/http"
)
/*
 * browser http://localhost:8080/hello
 */
func hello(w http.ResponseWriter, req *http.Request) {
    outs := `
<html>
    <h3>Hello world!</h3>
</html>
`
    fmt.Fprintf(w, outs)
}

func headers(w http.ResponseWriter, req *http.Request) {

    for name, headers := range req.Header {
        for _, h := range headers {
            fmt.Fprintf(w, "%v: %v\n", name, h)
        }
    }
}
func world(w http.ResponseWriter, req *http.Request) {
    outs := `
<html>
    <h2>Hello world!</h2>
</html>
`
    fmt.Fprintf(w, outs)
}

func main() {
    ports := []string{ ":8080", ":9090" }

    httpsrv1(ports[0])
    httpsrv2(ports[1])

    /* Block Here */
    select {}
}

func httpsrv1(port string)  {
    mux := http.NewServeMux()
    mux.HandleFunc("/hello", hello)
    mux.HandleFunc("/headers", headers)
    /*
     * ListenAndServe will block current routine
     * start a new routine for it
     */
    go http.ListenAndServe(port, mux)
}

func httpsrv2(port string) {
    mux := http.NewServeMux()
    mux.HandleFunc("/world", world)
    go http.ListenAndServe(port, mux)
}