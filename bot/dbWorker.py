import sqlite3


class SQLighter:
    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

    def create(self):
        try:
            sql = """CREATE TABLE "notes" (
                        "chat_id"	TEXT NOT NULL,
                        "header"	TEXT,
                        "text"	TEXT,
                        "status"	INTEGER NOT NULL DEFAULT 0,
                        "time"	TEXT,
                        "id"	INTEGER
                    )"""
            self.cursor.execute(sql)
        except sqlite3.Error as e:
            print(f'Error: {e}')
            return False
        return True

    def add(self, data):
        try:
            sql = f"""INSERT INTO notes
                        VALUES ('{data[0]}', '{data[1]}', '{data[2]}',
                      '{data[3]}', '{data[4]}', '{data[5]}')"""
            self.cursor.execute(sql)
            self.connection.commit()
            print('Values added successfully')
        except sqlite3.Error as e:
            print(f'Error: {e}')
            return False
        return True

    def get(self, parameter, value):
        try:
            sql = f"SELECT * FROM notes WHERE {parameter}=?"
            self.cursor.execute(sql, [value])
        except sqlite3.Error as e:
            print(f'Error: {e}')
            return None
        return self.cursor.fetchall()

    def delete(self, parameter, value):
        try:
            sql = f"DELETE FROM notes WHERE {parameter}=?"
            self.cursor.execute(sql, [value])
            self.connection.commit()
            print('Note has been deleted successfully')
        except sqlite3.Error as e:
            print(f'Error: {e}')
            return False
        return True

    def close(self):
        self.connection.close()
