#!/usr/bin/env python

import contextlib
import itertools
import os
import re
import sqlite3

import nltk
from nltk.corpus import wordnet as wn

import constants


@contextlib.contextmanager
def get_connection(path):
    conn = sqlite3.connect(path)
    conn.execute("DROP TABLE IF EXISTS words")
    conn.execute("CREATE TABLE words (word TEXT UNIQUE, type INT, source INT)")
    try:
        yield conn
    finally:
        conn.commit()
        conn.execute("CREATE INDEX words_type ON words (type)")
        conn.execute("CREATE INDEX words_source ON words (source)")
        conn.commit()
        conn.execute("ANALYZE")
        conn.close()

# http://codegolf.stackexchange.com/questions/47322/how-to-count-the-syllables-in-a-word
get_number_of_syllables = lambda w:len(''.join(" x"[c in"aeiouy"] for c in w.rstrip('e')).split())


def is_word_acceptable(word, token_min_length, token_max_length, maximum_syllables):
    return re.match("^[a-z]{%s,%s}$" % (token_min_length, token_max_length), word) \
        and get_number_of_syllables(word) <= maximum_syllables 


def get_dictionary_words(path="/usr/share/dict/words",
                         token_min_length=constants.TOKEN_MIN_LENGTH,
                         token_max_length=constants.TOKEN_MAX_LENGTH,
                         maximum_syllables=constants.MAXIMUM_SYLLABLES):
    with open("/usr/share/dict/words") as f_in:
        lines = (line.strip().lower() for line in f_in)
        good_lines = (line for line in lines
            if is_word_acceptable(line, token_min_length, token_max_length, maximum_syllables))
        for word in good_lines:
            pos_type = nltk.pos_tag([word])[0][1]
            yield (word, pos_type, "DICTIONARY")


def get_wordnet_words(token_min_length=constants.TOKEN_MIN_LENGTH,
                      token_max_length=constants.TOKEN_MAX_LENGTH,
                      maximum_syllables=constants.MAXIMUM_SYLLABLES):
    wordnet_type_to_pos_type = {
        wn.NOUN: "NN",
        wn.ADJ: "JJ",
    }
    for wordnet_type, pos_type in wordnet_type_to_pos_type.items():
        for synset in wn.all_synsets(wordnet_type):
            word = synset.name().split(".")[0].lower()
            if is_word_acceptable(word, token_min_length, token_max_length, maximum_syllables):
                yield (word, pos_type, "WORDNET")


def get_pos_tag(word):
    return nltk.pos_tag([word])[0][1]


def insert_word(conn, word, tag, source):
    c = conn.cursor()
    tag_type = constants.POS_TYPE_TO_INT[tag]
    source_type = constants.SOURCE_TO_INT[source]
    c.execute("INSERT OR IGNORE INTO words VALUES (?, ?, ?)", (word, tag_type, source_type))


def main():
    with get_connection(constants.DB_PATH) as conn:
        source_data = itertools.chain(
            get_wordnet_words(),
            #get_dictionary_words(),
        )
        for i, (word, pos_type, word_source) in enumerate(source_data):
            if pos_type in constants.POS_TYPE_TO_INT:
                insert_word(conn, word, pos_type, word_source)
            if i % 1000 == 0:
                conn.commit()

if __name__ == "__main__":
    main()
