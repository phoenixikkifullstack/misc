package main

import (
    "fmt"
    "os"
    "path/filepath"
)

func check(e error) {
    if e != nil {
        panic(e)
    }
}

func main() {

    f, err := os.CreateTemp("", "sample")
    check(err)

    fmt.Println("Temp file name:", f.Name())

    defer os.Remove(f.Name())
    defer f.Close()

    // _, err = f.Write([]byte{1, 2, 3, 4})
    str := "hello world"
    _, err = f.Write([]byte(str))
    check(err)

    dname, err := os.MkdirTemp("", "sampledir")
    check(err)
    fmt.Println("Temp dir name:", dname)

    defer os.RemoveAll(dname)

    fname := filepath.Join(dname, "file1")
    err = os.WriteFile(fname, []byte{1, 2}, 0666)
    check(err)

    // f.Close()
    // err1 := os.Remove(f.Name())
    // if nil != err1 {
    //     fmt.Println("tmp file remove failed...", err1)
    // }

}