#!/usr/bin/env python

import os

DB_PATH = os.path.join(os.path.dirname(__file__), "words.db")
POS_TYPE_TO_INT = {
    "NN": 0,
    "JJ": 1
}
SOURCE_TO_INT = {
    "DICTIONARY": 0,
    "WORDNET": 1,
}
TOKEN_MIN_LENGTH = 4
TOKEN_MAX_LENGTH = 10
MAXIMUM_SYLLABLES = 3
