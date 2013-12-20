package model

import (
    "database/sql"
)

type DatabaseWordSource struct {
    db *DB
}

func NewDatabaseWordSource(db) *DatabaseWordSource {
    source := new(DatabaseWordSource)
    source.db = db
    return source
}

func RandomWord(source *DatabaseWordSource) (*Word, error) {
    rows, err := source.db.Query("SELECT * FROM words ORDER BY random() LIMIT 1")

    if err != nil {
        return nil, err
    }

    var word *Word = new(Word)
    rows.Next()
    err = rows.scan(&Word.Id, &Word.Word)

    return word, err
}

func AllWords(source *DatabaseWordSource) ([]Word, error) {
    rows, err := source.db.Query("SELECT * FROM words")

    if err != nil {
        return nil, err
    }

    var words []Word

    for rows.Next() {
        var word *Word = new(Word)
        err = rows.Scan(&word.Id, &word.Word)
        if err != nil {
            return nil, err
        }
        append(words, word)
    }

    return words, nil
}
