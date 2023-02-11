import unittest
from bot_db import *


class TestDataBase(unittest.TestCase):

    def test_upper(self):
        self.db_test = DataBase('user_bot')
        self.add = self.db_test.add_account('Vasyar', '937475')

    def test_add_users_db(self):
        self.assertNotEqual(self.db_test.add_account('Vasyar', '94750'), 11)


if __name__ == '__main__':
    unittest.main()
