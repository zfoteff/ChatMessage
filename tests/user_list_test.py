"""Test suite for unittesting the UserList class"""

__version__ = "1.0.0."
__author__ = "Zac Foteff"

import unittest
import time
from bin.logger import Logger
from bin.constants import *
from src.users import ChatUser
from src.user_list import UserList

log = Logger("./userListTest")

class UserListTests(unittest.TestCase):
    """Test cases for UserList class object alone"""

    def setUp(self) -> None:
        return super().setUp()

    def test_db_connection(self):
        pass

class UserListWithChatUserTest(unittest.TestCase):
    """Test cases for UserList class object with ChatUser objects"""

    def setUp(self) -> None:
        return super().setUp()

    def test_both_db_connection(self):
        pass