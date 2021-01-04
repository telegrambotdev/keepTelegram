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
                    "time"	TEXT,
                    "id"	INTEGER
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


def add(conn, cursor, data):
    try:
        sql = f"""INSERT INTO notes
                    VALUES ('{data[0]}', '{data[1]}', '{data[2]}',
                  '{data[3]}', '{data[4]}', '{data[5]}')"""
        cursor.execute(sql)
        conn.commit()
        print('Values added successfully')
    except sqlite3.Error as e:
        print(f'Error: {e}')
        return False
    return True


def get(cursor, parameter, value):
    try:
        sql = f"SELECT * FROM notes WHERE {parameter}=?"
        cursor.execute(sql, [value])
    except sqlite3.Error as e:
        print(f'Error: {e}')
        return None
    return cursor.fetchall()
