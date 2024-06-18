package main

import (
        _"errors"
		"fmt"
		"database/sql"
		"os/exec"
		"bytes"
		"strings"
        _"reflect"
		_"github.com/go-sql-driver/mysql"
		"github.com/jmoiron/sqlx"
)


type Users struct {
	Id		    int             `db:"id"`
	Name		string          `db:"name"`
	Password	string          `db:"password"`
	Type		[]uint8	        `db:"type"`
	Role		int             `db:"role"`
	Status		int             `db:"status"`
	Rem_token	sql.NullString	`db:"remember_token"`
	Create_time	sql.NullInt64	`db:"created_at"`
	Update_time	sql.NullInt64	`db:"updated_at"`
}

var Database *sqlx.DB

func main() {
    err := userSelect()
    if (err != nil) {
        fmt.Println("userSelect failed:", err)
    }

	Database.Close()
}

func userSelect() (error) {
    var users []Users

	err := Database.Select(&users, "select id,name,password,type,role,status,remember_token,created_at,updated_at from users limit 10")
	if err != nil {
		fmt.Println("exec failed, ", err)
		return err
	}

	// fmt.Println("select succ:", users)
	for _, value := range users {
		// fmt.Println(value);
        // fmt.Println(reflect.TypeOf(value.Create_time).Name(), reflect.TypeOf(value.Create_time).Kind())
        fmt.Printf("[%v][\"%s\"][\"%s\"]['%c'][%v][%v][\"%s\"][%v][%v]\n",
                    value.Id, value.Name, value.Password,
                    value.Type[0], value.Role, value.Status,
                    value.Rem_token.String, value.Create_time.Int64, value.Update_time.Int64)
    }

    return nil
}

func init() {
	// fmt.Println("00 Database:", Database)
	mysql_pwd, err := exec_shell("/zrtx/tools/getsqlpass | cut -c 1-14")
	if err != nil {
		fmt.Println("get mysql pwd failed,", err)
		return
	}
	// fmt.Println("pwd:", mysql_pwd)

	sql_conc_str := "root:" + strings.Replace(mysql_pwd,"\n","", -1) + "@tcp(127.0.0.1:3306)/realEyeServer"
	// fmt.Println("sql_conc_str:", sql_conc_str)

	database, err := sqlx.Connect("mysql", sql_conc_str)
	if err != nil {
		fmt.Println("open mysql/realEyeServer failed,", err)
        panic(err)
	}

    Database = database
	// fmt.Println("01 Database:", Database)
}

func exec_shell(s string) (string, error){
	cmd := exec.Command("/bin/bash", "-c", s)

	var out bytes.Buffer
	cmd.Stdout = &out

	err := cmd.Run()
	checkErr(err)

	return out.String(), err
}

func checkErr(err error) {
	if err != nil {
		fmt.Println(err)
		panic(err)
	}
}

