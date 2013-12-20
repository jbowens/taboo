package model

type Word struct {
    id int
    word string
}

func (w *Word) Id() int {
    return w.id
}

func (w *Word) Word() string {
    return w.word
}
