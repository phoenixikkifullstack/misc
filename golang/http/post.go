package main

import (
    "fmt"
    "net/http"
    "strings"
    "io/ioutil"
)

const (
    dga_url = "http://127.0.0.1:8000"
)

func verify() {
    // url := "http://10.2.55.6:8000/verify/"
    url := dga_url + "/verify/"

    payload := strings.NewReader("{\"domain\":\"xyzfdsabsddfasgsdagsdagsadfds.com\"}")

    req, _ := http.NewRequest("POST", url, payload)

    req.Header.Add("Content-Type", "application/json")

    response, err := http.DefaultClient.Do(req)
    if nil != err {
        fmt.Printf("err:[%#v]\n", err)
        return
    }

    // fmt.Printf("\t|==>> StatusCode:[%#v]\n", response.StatusCode)
    // fmt.Printf("\t|==>> Header:[%#v]\n", response.Header)
    body, _ := ioutil.ReadAll(response.Body)
    // fmt.Println(string(body))
    fmt.Printf("\t|==>> Url:[%#v]\n", url)
    fmt.Printf("\t|==>> Payload:[%#v]\n", payload)
    fmt.Printf("\t|==>> Status:[%#v]\n", response.Status)
    fmt.Printf("\t|==>> Body:[%s]\n", string(body))

    defer response.Body.Close()

    return
}

func listAllApi() {
    // url := "http://10.2.55.6:8000/list_all_api/"
    url := dga_url + "/list_all_api/"

    payload := strings.NewReader("")

    req, _ := http.NewRequest("POST", url, payload)

    req.Header.Add("Content-Type", "application/json")

    response, err := http.DefaultClient.Do(req)
    if nil != err {
        fmt.Printf("err:[%#v]\n", err)
        return
    }

    // fmt.Printf("\t|==>> StatusCode:[%#v]\n", response.StatusCode)
    // fmt.Printf("\t|==>> Header:[%#v]\n", response.Header)
    body, _ := ioutil.ReadAll(response.Body)
    // fmt.Println(string(body))
    fmt.Printf("\t|==>> Url:[%#v]\n", url)
    fmt.Printf("\t|==>> Payload:[%#v]\n", payload)
    fmt.Printf("\t|==>> Status:[%#v]\n", response.Status)
    fmt.Printf("\t|==>> Body:[%s]\n", string(body))

    defer response.Body.Close()

    return
}

func main() {
    fmt.Printf("\t|-------------------------------\n")
    listAllApi()
    fmt.Printf("\t|-------------------------------\n")
    verify() 
    fmt.Printf("\t|-------------------------------\n")
}

