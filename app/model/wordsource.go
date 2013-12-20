package model

// An interface for accessing words.
type WordSource interface {

    // Retrieves a random word
    RandomWord() (*Word, error)

    // Retrieves all of the words from this word source
    AllWords() ([]*Word, error)

}
