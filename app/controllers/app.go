package controllers

import (
    "github.com/robfig/revel"
)

type App struct {
	*revel.Controller
}

func (c App) Index() revel.Result {

    return c.Render()

/*
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
*/
}
