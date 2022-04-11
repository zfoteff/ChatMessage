"""Test suite for unit testing the ChatUser class"""

__version__ = "2.0.0."
__author__ = "Zac Foteff"

import unittest
import time
from bin.logger import Logger
from src.chat_user import ChatUser

log = Logger("./chatUserTest")


class ChatUserTests(unittest.TestCase):
    """Test cases for ChatUser class object"""

    TEST_ALIAS = "zfoteff_test"

    def setUp(self) -> None:
        return super().setUp()

    def test_create_single_instance(self):
        """Create a single instance of a chat user test and assert it has the proper defaults
        """
        start_time = time.perf_counter()
        chat_user = ChatUser(self.TEST_ALIAS)
        log(str(chat_user))
        self.assertIsNotNone(chat_user)
        self.assertIsInstance(chat_user, ChatUser)
        self.assertEqual(chat_user.alias, self.TEST_ALIAS)
        self.assertEqual(chat_user.blocked_users, [])
        self.assertFalse(chat_user.removed)
        elapsed_time = time.perf_counter() - start_time
        log(str(chat_user), 'd')
        log(str(chat_user.to_dict()), 'd')
        log(f"[+] Completed create single instance test in {elapsed_time:.5f}")
