import unittest
from bot import dbWorker


class Path:
    """Parent class with the common field"""
    path = './database.db'


class DBTest1(unittest.TestCase, Path):
    """First class for testing work with database"""
    def test_create(self):
        """Test creation of database"""
        self.assertTrue(dbWorker.create_db(self.path))
        self.assertFalse(dbWorker.create_db(self.path))

    def test_conn(self):
        """Test connection to database"""
        self.assertIsNotNone(dbWorker.connect(self.path))


class DBTest2(unittest.TestCase, Path):
    """First class for testing work with database"""
    def test_add(self):
        """Test adding data to database"""
        conn = dbWorker.connect(self.path)
        cursor = conn.cursor()
        data = ['test_id', 'test_header', 'test_text', 1, 'test_time']
        self.assertTrue(dbWorker.add_note(conn, cursor, data))

    def test_get(self):
        """Test getting data from database"""
        conn = dbWorker.connect(self.path)
        cursor = conn.cursor()
        data = 'test_id'
        self.assertIsNotNone(dbWorker.get_notes(cursor, data))
        self.assertListEqual(dbWorker.get_notes(cursor, data),
                             [('test_id', 'test_header', 'test_text', 1, 'test_time')])
        self.assertListEqual(dbWorker.get_notes(cursor, ''), [])
