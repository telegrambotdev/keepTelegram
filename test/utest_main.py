import unittest
import dbWorker


class DBTest(unittest.TestCase):
    def test_create(self):
        self.assertTrue(dbWorker.create_db('./database.db'))
