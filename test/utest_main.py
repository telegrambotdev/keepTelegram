import os
import requests
import unittest
import time

from bot import dbWorker


class Parent:
    """Parent class with need variables"""
    path = './database.db'
    token = os.getenv('TELEGRAM_TOKEN')
    url = f'https://api.telegram.org/bot{token}/'
    ok_status_code = 200
    bot_name = 'Telegram Keep'
    chat_id = os.getenv('CHAT_ID')
    test_text = 'test'
    SQLighter = dbWorker.SQLighter(path)
    timestamp = time.time()


class DBTest1(unittest.TestCase, Parent):
    """First class for testing work with database"""

    def test_create(self):
        """Test creation of database"""
        self.assertTrue(self.SQLighter.create())
        self.assertFalse(self.SQLighter.create())

    def test_conn(self):
        """Test connection to database"""
        self.assertIsNotNone(dbWorker.SQLighter(self.path))


class DBTest2(unittest.TestCase, Parent):
    """Second class for testing work with database"""

    def test_add(self):
        """Test adding data to database"""
        data = [
            'test_id',
            'test_header',
            'test_text',
            1,
            'test_time',
            self.timestamp]
        self.assertTrue(self.SQLighter.add(data))

    def test_get(self):
        """Test getting data from database"""
        parameter = 'chat_id'
        data = 'test_id'
        self.assertIsNotNone(self.SQLighter.get(parameter, data))
        self.assertListEqual(
            self.SQLighter.get(
                parameter, data), [
                ('test_id', 'test_header', 'test_text', 1, 'test_time', self.timestamp)])
        self.assertListEqual(self.SQLighter.get(parameter, ''), [])

    def test_update(self):
        """Test updating the data"""
        parameter_to_set = 'chat_id'
        value_to_set = 'test_id1'
        parameter_to_search = 'chat_id'
        value_to_search = 'test_id'
        self.assertTrue(self.SQLighter.update(parameter_to_set, value_to_set, parameter_to_search, value_to_search))
        self.assertFalse(self.SQLighter.update('', '', '', ''))
        self.assertFalse(self.SQLighter.update('', '', '', None))
        data = self.SQLighter.get(parameter_to_search, value_to_set)
        self.assertEqual(value_to_set, data[0][0])


class DBTest3(unittest.TestCase, Parent):
    """Second class for testing work with database"""

    def test_delete(self):
        """Test deleting data from database"""
        parameter = 'chat_id'
        data = 'test_id'
        self.assertTrue(self.SQLighter.delete(parameter, data))
        self.assertFalse(self.SQLighter.delete('', ''))
        self.assertListEqual(self.SQLighter.get(parameter, data), [])


class TelegramTest(unittest.TestCase, Parent):
    """Class for testing connecting with Telegram API"""

    def setUp(self):
        """Make requests"""
        self.getMe = requests.get(self.url + 'getMe')
        self.getUpdates = requests.get(self.url + 'getUpdates')
        self.sendMessage = requests.get(
            self.url + f'sendMessage?chat_id={self.chat_id}&text={self.test_text}')

    def test_conn(self):
        """Test connection with different methods"""
        self.assertEqual(self.getMe.status_code, self.ok_status_code)
        self.assertEqual(self.getUpdates.status_code, self.ok_status_code)
        self.assertEqual(self.sendMessage.status_code, self.ok_status_code)

    def test_fields(self):
        """Test fields from different request methods"""
        self.assertTrue(self.getMe.json()["ok"])
        self.assertTrue(self.getUpdates.json()["ok"])
        self.assertTrue(self.sendMessage.json()["ok"])
        self.assertTrue(self.getMe.json()["result"]["is_bot"])
        self.assertFalse(
            self.getMe.json()["result"]["can_read_all_group_messages"])
        self.assertFalse(
            self.getMe.json()["result"]["supports_inline_queries"])
        self.assertEqual(
            self.getMe.json()["result"]["first_name"],
            self.bot_name)
        self.assertEqual(
            self.sendMessage.json()["result"]["text"],
            self.test_text)
