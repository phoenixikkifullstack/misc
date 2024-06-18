package main

import (
    "rules/idsrules"
    "log"
)

func main() {
    line := `alert tcp $TELNET_SERVERS 23 -> $EXTERNAL_NET any (msg:"GPL TELNET TELNET login failed"; flow:from_server,established; content:"Login failed"; nocase; classtype:bad-unknown; sid:2100492; rev:10;)`
    rule, err := idsrules.Parse(line)
    if err != nil {
        log.Fatal(err)
    }
    log.Printf("Rule 【%s】 is enable: %v", rule.Msg, rule.Enabled)

}