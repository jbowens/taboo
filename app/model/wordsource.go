package model

// An interface for accessing words.
type WordSource interface {

    // Retrieves a random word
    RandomWord() (*Word, error)

    // Retrieves all of the words from this word source
    AllWords() ([]*Word, error)

    // Counts how many words are provided by this source
    Count() int

    // Retrieves the lexicographically n-th word in the source
    GetWord(n int) (*Word, error)

}
