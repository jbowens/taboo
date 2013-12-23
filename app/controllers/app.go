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

    db, err := sql.Open("postgres", "user=prod dbname=prod password=lol sslmode=disable")
    if err != nil {
        log.Fatal(err)
    }

    source := model.NewDatabaseWordSource(db)
    word, err := source.RandomWord()

    if err != nil {
        log.Fatal(err)
    }

	return c.Render(word)
}
