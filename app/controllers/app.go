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

    db, err := sql.Open("postgres", "user=taboo dbname=taboo password=ilovetaboo sslmode=disable")
    if err != nil {
        log.Fatal(err)
    }

    source := model.NewDatabaseWordSource(db)
    word, err := source.RandomWord()

	return c.Render(word)
}
