package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"math/rand"
	"net"
	"os"
	"path/filepath"
	"time"

	"github.com/gobwas/ws"
	"github.com/gobwas/ws/wsutil"
)

var (
	mock map[string][]byte
)

func serve(conn net.Conn) {
	defer func() {
		_ = conn.Close()
	}()

	for {
		b, code, err := wsutil.ReadClientData(conn)
		if err != nil {
			printLogF("ERROR [READ]: %s", err)
			break
		}

		t := time.Second
		printLogF("DATA [READ]: n=%d code=%d", b, code)

		r, ok := matchMock(b)
		if !ok {
			r = "unknown"
			t += time.Duration(rand.Int() % 1000) * time.Millisecond
		}

		time.Sleep(t)
		if err = wsutil.WriteServerText(conn, []byte(r)); err != nil {
			printLogF("ERROR [WRITE]: %s", err)
		}
	}
}

func makeMock(d string) map[string][]byte {
	m := make(map[string][]byte)

	fs, err := ioutil.ReadDir(d)
	if err != nil {
		log.Fatal(err)
	}
	for _, f := range fs {
		b, err := ioutil.ReadFile(filepath.Join(d, f.Name()))
		if err != nil {
			log.Fatal(err)
		}
		m[f.Name()] = b
	}

	return m
}

func matchMock(b []byte) (string, bool) {
	for k, v := range mock {
		if len(v) != len(b) {
			continue
		}

		ok := true
		for i := 0; i < len(v); i++ {
			if v[i] != b[i] {
				ok = false
				break
			}
		}
		if ok {
			return k, true
		}
	}
	return "", false
}

func main() {
	addr, path := os.Args[1], os.Args[2]
	mock = makeMock(path)

	ln, err := net.Listen("tcp", addr)
	if err != nil {
		log.Fatal(err)
	}
	u := ws.Upgrader{
		OnHeader: func(key, value []byte) (err error) {
			log.Printf("non-websocket header: %q=%q", key, value)
			return
		},
	}
	for {
		conn, err := ln.Accept()
		if err != nil {
			printLogF("ERROR [ACCEPT]: %s", err)
			break
		}

		_, err = u.Upgrade(conn)
		if err != nil {
			printLogF("ERROR [UPGRADE]: %s", err)
			break
		}

		go serve(conn)
	}
}

func printLogF(format string, v ...interface{}) {
	log.Println(fmt.Sprintf(format, v...))
}
