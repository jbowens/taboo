package model

import (
    "errors"
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

func (s *InMemoryWordSource) Count() int {
    return len(s.words)
}

func (s *InMemoryWordSource) GetWord(n int) (*Word, error) {
    if n >= len(s.words) {
      return nil, errors.New("Index exceeds word source's word count.")
    }
    return s.words[n], nil
}
