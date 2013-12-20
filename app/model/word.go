package model

import (
    "math/rand"
)

type Word struct {
    id          int
    word        string
    prohibited  []string
}

func (w *Word) Id() int {
    return w.id
}

func (w *Word) Word() string {
    return w.word
}

func (w *Word) ProhibitedWords() []string {
    return w.prohibited
}

func (w *Word) SampleProhibitedWords() []string {
    perm := rand.Perm(len(w.prohibited))
    sample := make([]string, 5)
    for i := 0; i < 5; i++ {
        sample[i] = w.prohibited[perm[i]] 
    }
    return sample
}
