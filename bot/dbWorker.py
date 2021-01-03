import sqlite3


def create_db(path):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    try:
        sql = """CREATE TABLE "notes" (
                    "chat_id"	TEXT NOT NULL,
                    "header"	TEXT,
                    "text"	TEXT,
                    "status"	INTEGER NOT NULL DEFAULT 0,
                    "time"	TEXT
                )"""
        cursor.execute(sql)
        return True
    except sqlite3.Error as e:
        print(f'Error: {e}')
        return False


def connect(path):
    try:
        conn = sqlite3.connect(path)
        print('Connection is successful')
    except sqlite3.Error as e:
        print(f'Error: {e}')
        return None
    return conn


def add_note(conn, cursor, data):
    try:
        sql = f"""INSERT INTO notes
                    VALUES ('{data[0]}', '{data[1]}', '{data[2]}',
                  '{data[3]}', '{data[4]}')"""
        cursor.execute(sql)
        conn.commit()
        print('Values added successfully')
    except sqlite3.Error as e:
        print(f'Error: {e}')
        return False
    return True


def get_notes(cursor, chat_id):
    try:
        sql = "SELECT * FROM notes WHERE chat_id=?"
        cursor.execute(sql, [chat_id])
    except sqlite3.Error as e:
        print(f'Error: {e}')
        return None
    return cursor.fetchall()
