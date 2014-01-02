package controllers

import (
    "crypto/rand"
    "math/big"
    "database/sql"
    "log"
    "strconv"
    "github.com/jbowens/taboo/app/model"
    "github.com/robfig/revel"
    _ "github.com/lib/pq"
)

type Api struct {
	*revel.Controller
}

func (c Api) randString(n int) string {
    const alphanum = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    symbols := big.NewInt(int64(len(alphanum)))
    states := big.NewInt(0)
    states.Exp(symbols, big.NewInt(int64(n)), nil)
    r, err := rand.Int(rand.Reader, states)
    if err != nil {
        panic(err)
    }
    var bytes = make([]byte, n)
    r2 := big.NewInt(0)
    symbol := big.NewInt(0)
    for i := range bytes {
        r2.DivMod(r, symbols, symbol)
        r, r2 = r2, r
        bytes[i] = alphanum[symbol.Int64()]
    }
    return string(bytes)
}

func (c Api) Cards() revel.Result {

    db, err := sql.Open("postgres", "user=prod dbname=prod password=lol sslmode=disable")
    if err != nil {
        log.Fatal(err)
    }

    source := model.NewDatabaseWordSource(db)
    word, err := source.RandomWord()

    if err != nil {
        log.Fatal(err)
    }

	return c.RenderJson(word)
}

func (c Api) Register() revel.Result {

    db, err := sql.Open("postgres", "user=prod dbname=prod password=lol sslmode=disable")
    if err != nil {
        log.Fatal(err)
    }

    key := c.randString(64) 

    stmt, err := db.Prepare("INSERT INTO installs (key) VALUES($1) RETURNING id")
    if err != nil {
        log.Fatal(err)
    }

    var id int
    err = stmt.QueryRow(key).Scan(&id);
    if err != nil {
        log.Fatal(err)
    }

    return c.RenderJson(struct {
        InstallReference string     `json:'install_reference'`
    }{strconv.Itoa(id) + "-" + key});
}
