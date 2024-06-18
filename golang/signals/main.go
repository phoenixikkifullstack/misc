package main

// signal samples from https://gobyexample.com/signals

import (
    "fmt"
    "os"
    "os/signal"
    "syscall"
    "time"
)

type l_contex struct {
    sigs chan os.Signal
    done chan bool
}

var ctx l_contex

func main() {
    contex_init(&ctx)

    /* signal handle routine */
    go sig_handler(&ctx)

    /* Main Loop */
    main_loop(&ctx)

    /* deinit before exit */
    contex_deinit(&ctx)

    os.Exit(0)
}

func contex_init(contex *l_contex) {
    contex.done = make(chan bool, 1)
    contex.sigs = signal_reg()
}

func signal_reg() chan os.Signal {
    sigs := make(chan os.Signal, 1)

    signal.Notify(sigs, syscall.SIGINT)
    signal.Notify(sigs, syscall.SIGTERM)

    return sigs
}

func sig_handler(contex *l_contex) {
    F_EXIT: for {
        select {
        case sig := <-contex.sigs:
            switch sig {
                case syscall.SIGINT:
                    fmt.Println("Received SIGINT signal.")
                    break F_EXIT
                case syscall.SIGTERM:
                    fmt.Println("Received SIGTERM signal.")
                    break F_EXIT
                default:
                    fmt.Println("Received unknown signal.")
            }
        }
    }
    contex.done <- true
}

func main_loop(contex *l_contex) {
    EXIT: for {
        select {
        case <- contex.done:
            fmt.Println("Exiting...")
            break EXIT
        default:
            // main loop
            time.Sleep(100 * time.Millisecond)
        }
    }
}

func contex_deinit(contex *l_contex) {
    close(contex.sigs)
    close(contex.done)
}