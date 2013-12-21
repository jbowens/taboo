#!/usr/bin/python
from stemming.porter2 import stem
import DictionaryServices, re, operator

ignore_list = set(['the', 'noun', 'adjective', 'the', 'for', 'not', 'when', 'shall', 'will', 'and', 'with', 'brit', 'informal', 'but', 'that', 'from', 'verb', 'their'])

start = "love"
max_depth = 10
min_word_len = 4

visited = set([])
freqs = dict()

def visit(word, depth):
    if depth > max_depth:
        return
    if word in visited:
        return

    word_stem = stem(word)

    visited.add(word)

    if not word in freqs:
        freqs[word] = dict()

    text = DictionaryServices.DCSCopyTextDefinition(None, word, (0, len(word)))
    if not text or len(text) == 0:
        return

    filtered_text = re.sub(r'[\W\d]+', ' ', text).lower()
    words = filtered_text.split()
    
    for w in words:
        w_stem = stem(w)
        if w not in ignore_list and len(w) >= min_word_len and w != word and w_stem != word_stem:
            if not w in freqs:
                freqs[w] = dict()

            freqs[word][w] = 1 if w not in freqs[word] else freqs[word][w] + 1
            freqs[w][word] = 1 if word not in freqs[w] else freqs[w][word] + 1
            
            visit(w, depth + 1)

visit(start, 1)

sorted_words = sorted(freqs.keys())
for word in sorted_words:
    if len(freqs[word]) >= 5:
        x = sorted(freqs[word].iteritems(), key=operator.itemgetter(1), reverse=True)
        sorted_matches = map(lambda x: x[0], x)
        print word + ': ' + ', '.join(sorted_matches[0:5])

