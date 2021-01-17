"""File for work with database."""
import sqlite3


class SQLighter:
    """Main class with all necessary methods"""

    def __init__(self, path):
        """Create the connection"""
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

    def create(self):
        """Create a table in database."""
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
        except sqlite3.Error as error:
            print(f'Error: {error}')
            return False
        return True

    def add(self, data):
        """Insert data to database."""
        try:
            sql = f"""INSERT INTO notes
                        VALUES ('{data[0]}', '{data[1]}', '{data[2]}',
                      '{data[3]}', '{data[4]}', '{data[5]}')"""
            self.cursor.execute(sql)
            self.connection.commit()
            print('Values added successfully')
        except sqlite3.Error as error:
            print(f'Error: {error}')
            return False
        return True

    def get(self, parameter, value):
        """Get data from database."""
        try:
            sql = f"SELECT * FROM notes WHERE {parameter}=?"
            self.cursor.execute(sql, [value])
        except sqlite3.Error as error:
            print(f'Error: {error}')
            return None
        return self.cursor.fetchall()

    def update(
            self,
            parameter_to_set,
            value_to_set,
            parameter_to_search,
            value_to_search):
        """Update data in a database."""
        try:
            sql = f"UPDATE notes SET {parameter_to_set}=? WHERE {parameter_to_search}=?"
            self.cursor.execute(sql, [value_to_set, value_to_search])
            self.connection.commit()
            print('Values updated successfully')
        except sqlite3.Error as error:
            print(f'Error: {error}')
            return False
        return True

    def delete(self, parameter, value):
        """Delete data from a database."""
        try:
            sql = f"DELETE FROM notes WHERE {parameter}=?"
            self.cursor.execute(sql, [value])
            self.connection.commit()
            print('Note has been deleted successfully')
        except sqlite3.Error as error:
            print(f'Error: {error}')
            return False
        return True

    def close(self):
        """Close connection with a database."""
        self.connection.close()
