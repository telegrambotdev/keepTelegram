import unittest
from bot.dbWorker import create_db


class DBTest(unittest.TestCase):
    def test_create(self):
        self.assertTrue(create_db('./database.db'))
