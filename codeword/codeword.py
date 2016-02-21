#!/usr/bin/env python

import constants
import contextlib
import random
import sqlite3


@contextlib.contextmanager
def get_connection(path):
    conn = sqlite3.connect(path)
    try:
        yield conn
    finally:
        conn.close()


def get_noun(conn):
    return get_word(conn, "NN")


def get_adjective(conn):
    return get_word(conn, "JJ")


def get_word(conn, pos_type):
    c = conn.cursor()
    c.execute("SELECT word FROM words WHERE type = ? ORDER BY RANDOM() LIMIT 1", (constants.POS_TYPE_TO_INT[pos_type], ))
    return c.fetchone()[0]


def get_codeword(conn):
    if random.random() > 0.5:
        words = [get_noun(conn), get_noun(conn)]
    else:
        words = [get_adjective(conn), get_noun(conn)]
    return " ".join(words)


if __name__ == "__main__":
    with get_connection(constants.DB_PATH) as conn:
        print(get_codeword(conn))
