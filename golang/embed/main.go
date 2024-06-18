package main

import (
    _ "embed"
)

//go:embed string.txt
var string_str string
//go:embed byte.txt
var byte_text []byte

func test00() {
    println("-------------string------------------")
    println(string_str)
    println("-------------byte  ------------------")
    println(string(byte_text))
    println("------------------ ------------------")

}

func main() {
    test00()
}