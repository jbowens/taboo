package model

import (
    "math/rand"
)

type InMemoryWordSource struct {
    words     []*Word 
}

func NewInMemoryWordSource(words []*Word) *InMemoryWordSource {
    source := new(InMemoryWordSource)
    source.words = words
    return source
}

func (s *InMemoryWordSource) RandomWord() (*Word, error) {
    indx := rand.Intn(len(s.words))
    return s.words[indx], nil
}

func (s *InMemoryWordSource) AllWords() ([]*Word, error) { 
    return s.words, nil
}
