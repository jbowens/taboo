#!/usr/bin/python
from stemming.porter2 import stem
import DictionaryServices, re, operator

#ignore_list = set(['the', 'noun', 'adjective', 'the', 'for', 'not', 'when', 'shall', 'will', 'and', 'with', 'brit', 'informal', 'but', 'that', 'from', 'verb', 'their', 'derivatives', 'adverb', 'late', 'latin', 'origin'])

start = "love"
max_depth = 10
min_word_len = 3
most_freq_cutoff = 100

visited = set([])
freqs = dict()
stems = dict()
unigram_freqs = dict()

def visit(word, depth):
    if depth > max_depth:
        return
    if word in visited:
        return

    word_stem = stem(word)

    visited.add(word)

    if not word in freqs:
        freqs[word] = dict()
        stems[word] = dict()

    text = DictionaryServices.DCSCopyTextDefinition(None, word, (0, len(word)))
    if not text or len(text) == 0:
        return

    filtered_text = re.sub(r'[\W\d]+', ' ', text).lower()
    words = filtered_text.split()
    
    for w in words:
        w_stem = stem(w)
        if w != word and len(w) >= min_word_len and w_stem != word_stem:
            if not w in freqs:
                freqs[w] = dict()
                stems[w] = dict()

            if w_stem not in stems[word]:
                freqs[word][w] = 1 if w not in freqs[word] else freqs[word][w] + 1
                stems[word][w_stem] = w
            else:
                same_stem = stems[word][w_stem]
                freqs[word][same_stem] = freqs[word][same_stem] + 1

            if word_stem not in stems[w]:
                freqs[w][word] = 1 if word not in freqs[w] else freqs[w][word] + 1
                stems[w][word_stem] = word
            else:
                same_stem = stems[w][word_stem]
                freqs[w][same_stem] = freqs[w][same_stem] + 1

            unigram_freqs[w] = 1 if w not in unigram_freqs else unigram_freqs[w] + 1
            
            visit(w, depth + 1)

visit(start, 1)

# Find the words that appeared most frequently. They're probably shit.
shit_words = map(lambda x: x[0], sorted(unigram_freqs.iteritems(), key=operator.itemgetter(1), reverse=True)[0:most_freq_cutoff])

# Remove shit words
for shit_word in shit_words:
    del freqs[shit_word]
    for w in freqs:
        if shit_word in freqs[w]:
            del freqs[w][shit_word]

sorted_words = sorted(freqs.keys())
for word in sorted_words:
    if len(freqs[word]) >= 5:
        x = sorted(freqs[word].iteritems(), key=operator.itemgetter(1), reverse=True)
        sorted_matches = map(lambda x: x[0], x)
        print word + ': ' + ', '.join(sorted_matches[0:5])

