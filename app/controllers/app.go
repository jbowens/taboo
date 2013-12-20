package controllers

import (
    "database/sql"
    "log"
    "github.com/robfig/revel"
    _ "github.com/lib/pq"
)

type App struct {
	*revel.Controller
}

func (c App) Index() revel.Result {

    db, err := sql.Open("postgres", "user=taboo dbname=taboo password=tababooboo sslmode=disable")
    if err != nil {
        log.Fatal(err)
    }

    rows, err := db.Query("SELECT * FROM words ORDER BY random() LIMIT 1")
    if err != nil {
        log.Fatal(err)
    }

    rows.Next()

    var id int
    var word string
    err = rows.Scan(&id, &word)

    if err != nil {
        log.Fatal(err)
    }

	return c.Render(word)
}
