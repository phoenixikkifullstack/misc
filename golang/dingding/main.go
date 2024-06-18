package main

import (
    "fmt"
    "github.com/blinkbean/dingtalk"
    _"net/http"
)

type dingding struct {
    token string
    secret string
} 

var ding_s dingding = dingding {
    token: "dd8cc07d5120d548dfccd592ee93232c480cfb4526800496d7db69e1a5aa4e3b",
    secret: "SEC0d18dbb99968ddbd6e0a85eb08e51e362477d2d5e6d1ac6d8eeda977081fc842",
}
// var dingToken = []string{"dd8cc07d5120d548dfccd592ee93232c480cfb4526800496d7db69e1a5aa4e3b"}
//var dingToken = []string{"0471c091acf1d9dfc553e57525f57139859858b905836b8f45b228e6d6e3a289"} // onlyOne

// var dingTalkCli = dingtalk.InitDingTalk(dingToken, ".")
// var dingTalkCliWithSecret = dingtalk.InitDingTalkWithSecret("dd8cc07d5120d548dfccd592ee93232c480cfb4526800496d7db69e1a5aa4e3b", "SECbbf4e0f661ca44b6b7bb8e8c04b74cf2aa93c88fcd6e09da2789d3cba743cd76") // 加签
var dingTalkCliWithSecret = dingtalk.InitDingTalkWithSecret(ding_s.token, ding_s.secret)

var testImg = "https://golang.google.cn/lib/godoc/images/footer-gopher.jpg"
var testUrl = "https://golang.google.cn/"
var testPhone = "18010*"

func textMsgWithSecret() {
    // err := dingTalkCliWithSecret.SendTextMessage("加签测试", dingtalk.WithAtMobiles([]string{testPhone}))
    err := dingTalkCliWithSecret.SendTextMessage("我看你TM是为难我胖虎！！！", dingtalk.WithAtMobiles([]string{testPhone}))
    if err != nil {
        fmt.Println("textMsgWithSecret expected be nil, but %v got", err)
    }
}

func main() {
    textMsgWithSecret()
    fmt.Println("HEWL")
}