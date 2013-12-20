package controllers

import (
    "database/sql"
    "log"
    "github.com/jbowens/taboo/app/model"
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

    var wordRow Word
    rows.Scan(&wordRow)
    word := wordRow.word

	return c.Render(word)
}
