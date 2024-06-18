package main

import (
    "strings"
    "os/exec"
    "log"
    "fmt"
    "reflect"
)
func main() {
    var out strings.Builder
    cmd := exec.Command("pwd")
    cmd.Stdout = &out

    err := cmd.Run()
    if err != nil {
        log.Fatal(err)
    }
    // fmt.Printf("[===>>]: %s", out.String())
    // fmt.Printf("[===>>]: %q", out.String())
    fmt.Print("[===>>]:", out.String())
    fmt.Println("[===>>]:", cmd.ProcessState)
    fmt.Println("type:", reflect.TypeOf(cmd.ProcessState));
}