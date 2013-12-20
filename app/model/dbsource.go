package model

import (
    "database/sql"
)

type DatabaseWordSource struct {
    db *sql.DB
}

func NewDatabaseWordSource(db *sql.DB) *DatabaseWordSource {
    source := new(DatabaseWordSource)
    source.db = db
    return source
}

func (source *DatabaseWordSource) RandomWord() (*Word, error) {
    rows, err := source.db.Query("SELECT * FROM words ORDER BY random() LIMIT 1")

    if err != nil {
        return nil, err
    }

    var word *Word = new(Word)
    rows.Next()
    err = rows.Scan(&word.id, &word.word)

    return word, err
}

func (source *DatabaseWordSource) AllWords() ([]*Word, error) {
    rows, err := source.db.Query("SELECT * FROM words")

    if err != nil {
        return nil, err
    }

    var words []*Word

    for rows.Next() {
        word := new(Word)
        err = rows.Scan(&word.id, &word.word)
        if err != nil {
            return nil, err
        }
        words = append(words, word)
    }

    return words, nil
}
