package main

import (
    "fmt"
    "ding2/dingtalk"
)

type dingding struct {
    token string
    secret string
} 

var ding_s = dingding {
    token: "dd8cc07d5120d548dfccd592ee93232c480cfb4526800496d7db69e1a5aa4e3b",
    secret: "SEC0d18dbb99968ddbd6e0a85eb08e51e362477d2d5e6d1ac6d8eeda977081fc842",
}

var dingTalkCliWithSecret = dingtalk.InitDingTalkWithSecret(ding_s.token, ding_s.secret)

// var testImg = "https://golang.google.cn/lib/godoc/images/footer-gopher.jpg"
// var testUrl = "https://golang.google.cn/"
var testPhone = "1801049*"
var testContent = `临江仙·滚滚长江东逝水
杨慎〔明代〕

滚滚长江东逝水，浪花淘尽英雄。是非成败转头空。青山依旧在，几度夕阳红。
白发渔樵江渚上，惯看秋月春风。一壶浊酒喜相逢。古今多少事，都付笑谈中。
`
var testContent1 = `石壕吏
杜甫〔唐代〕

暮投石壕村，有吏夜捉人。
老翁逾墙走，老妇出门看。
吏呼一何怒！妇啼一何苦！
听妇前致词：三男邺城戍。
一男附书至，二男新战死。
存者且偷生，死者长已矣！
室中更无人，惟有乳下孙。
有孙母未去，出入无完裙。
老妪力虽衰，请从吏夜归。
急应河阳役，犹得备晨炊。

夜久语声绝，如闻泣幽咽。
天明登前途，独与老翁别。
`

func textMsgWithSecret() {
    // err := dingTalkCliWithSecret.SendTextMessage("加签测试", dingtalk.WithAtMobiles([]string{testPhone}))
    // err := dingTalkCliWithSecret.SendTextMessage(testContent1, dingtalk.WithAtAll())
    err := dingTalkCliWithSecret.SendTextMessage(testContent1)
    if err != nil {
        e1 := fmt.Errorf("textMsgWithSecret expected be nil, but %v got", err)
        fmt.Printf("%#v", e1)
    }
}

func main() {
    textMsgWithSecret()
    fmt.Println("----------------------------")
}