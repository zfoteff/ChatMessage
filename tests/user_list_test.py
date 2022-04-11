"""Test suite for unit testing the UserList class"""

__version__ = "1.0.0."
__author__ = "Zac Foteff"

import unittest
import time
from bin.logger import Logger
from src.chat_user import ChatUser
from src.user_list import UserList

log = Logger("./userListTest")


class UserListTests(unittest.TestCase):
    """Test cases for UserList class object alone"""

    TEST_USER_LIST_NAME = "zfoteff_test_users"

    def setUp(self) -> None:
        return super().setUp()

    def test_db_connection(self):
        start_time = time.perf_counter()
        user_list = UserList(self.TEST_USER_LIST_NAME)
        try:
            user_list._mongo_client.server_info()
            elapsed_time = time.perf_counter() - start_time
            log(f"[+] Completed create single instance test in {elapsed_time:.5f}")
            self.assertTrue(True)
        except:
            elapsed_time = time.perf_counter() - start_time
            log(f"[-] MongoDB is not connected {elapsed_time:.5f}")
            self.fail()

    def test_create_single_instance(self):
        start_time = time.perf_counter()
        user_list = UserList(self.TEST_USER_LIST_NAME)
        self.assertIsNotNone(user_list)
        self.assertIsInstance(user_list, UserList)
        elapsed_time = time.perf_counter() - start_time
        log(f"[+] Completed create single instance test in {elapsed_time:.5f}")


class UserListWithChatUserTest(unittest.TestCase):
    """Test cases for UserList class object with ChatUser objects"""

    TEST_USER_ALIAS = "zfoteff_test"
    TEST_USER_LIST_NAME = "zfoteff_test_users"

    def setUp(self) -> None:
        return super().setUp()

    def test_register_single_user(self):
        start_time = time.perf_counter()
        user_list = UserList(self.TEST_USER_LIST_NAME)
        user_list.register(new_alias=self.TEST_USER_ALIAS)
        self.assertIn(self.TEST_USER_ALIAS, user_list.get_all_users())
        elapsed_time = time.perf_counter() - start_time
        log(f"[+] Completed register single user to user list in {elapsed_time:.5f}")

    def test_get_user(self):
        start_time = time.perf_counter()
        user_list = UserList(self.TEST_USER_LIST_NAME)
        user = user_list.get(self.TEST_USER_ALIAS)
        self.assertIsNotNone(user)
        self.assertIsInstance(user, ChatUser)
        elapsed_time = time.perf_counter() - start_time
        log(f"[+] Completed get user test in {elapsed_time:.5f}")
