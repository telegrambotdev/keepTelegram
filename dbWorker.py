import sqlite3


def connect(path):
    conn = sqlite3.connect(path)
    return conn.cursor()
