package model

import (
    "math/rand"
)

type Word struct {
    Id          int             `json:"id"`
    Word        string          `json:"word"`
    Prohibited  []string        `json:"prohibited_words"`
}

func (w *Word) ProhibitedWords() []string {
    return w.Prohibited
}

func (w *Word) SampleProhibitedWords() []string {
    perm := rand.Perm(len(w.Prohibited))
    sample := make([]string, 5)
    for i := 0; i < 5; i++ {
        sample[i] = w.Prohibited[perm[i]] 
    }
    return sample
}
