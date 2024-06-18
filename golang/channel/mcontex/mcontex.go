package mcontex

import "log"

var msg = make(chan bool)

func Wait_msg() {
    select {
    case <- msg:
    //     break
    // default:
    }
}

func Send_msg() {
    msg <- true
}

func init() {
    log.Println("hello from mcontex pkg...")
}