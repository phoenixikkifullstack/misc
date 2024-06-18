package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
)

var file_eve string = "./eve.json"

func main() {
	fp, err := os.OpenFile(file_eve, os.O_RDONLY, 6)
	if err != nil {
		fmt.Println("OpenFile failed,err:", err)
		return
	}
	defer fp.Close()

	n := 0
	r := bufio.NewReader(fp)
	for {
		// slice, err2 := r.ReadBytes('\n')
		_, err2 := r.ReadBytes('\n')
		n++
		// fmt.Print(string(slice))
		if err2 == io.EOF {
			break
		}
	}
	fmt.Printf("[==>>]n:%v\n", n)
	return
}
