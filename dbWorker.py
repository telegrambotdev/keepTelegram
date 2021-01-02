import sqlite3


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
        cursor.execute(f"""INSERT INTO notes
                          VALUES ('{data[0]}', '{data[1]}', '{data[2]}',
                          '{data[3]}', '{data[4]}')"""
                       )
        conn.commit()
        print('Values added successfully')
    except sqlite3.Error as e:
        print(f'Error: {e}')
        return False
    return True
