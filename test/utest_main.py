import unittest
from bot import dbWorker


class Path:
    path = './database.db'


class DBTest1(unittest.TestCase, Path):
    def test_create(self):
        self.assertTrue(dbWorker.create_db(self.path))

    def test_conn(self):
        self.assertIsNotNone(dbWorker.connect(self.path))


class DBTest2(unittest.TestCase, Path):
    def test_add(self):
        conn = dbWorker.connect(self.path)
        cursor = conn.cursor()
        data = ['test_id', 'test_header', 'test_text', 1, 'test_time']
        self.assertTrue(dbWorker.add_note(conn, cursor, data))

    def test_get(self):
        conn = dbWorker.connect(self.path)
        cursor = conn.cursor()
        data = 'test_id'
        self.assertIsNotNone(dbWorker.get_notes(cursor, data))
        self.assertListEqual(dbWorker.get_notes(cursor, data), [('test_id', 'test_header', 'test_text', 1, 'test_time')])
