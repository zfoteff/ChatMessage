"""Test suite for unit testing the Message Properties Class"""

__version__ = "1.0.0"
__author__ = "Zac Foteff"

import unittest
import time
import string
import random
from bin.logger import Logger
from bin.constants import *
from src.chat_room import ChatRoom

log = Logger("./chatRoomTest")
ROOM_NAME = "zfoteff_chatroom_tests"
ROOM_TYPE = CHAT_ROOM_TYPE_PUBLIC
OWNER_ALIAS = 'zfoteff'

class ChatRoomTests(unittest.TestCase):
    """Test cases for ChatRoom class object"""

    def setUp(self) -> None:
        return super().setUp()

    def generate_random_string(self, length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    def test_create_single_instance(self):
        start_time = time.perf_counter()
        room = ChatRoom(room_name=ROOM_NAME, room_type=ROOM_TYPE, owner_alias=OWNER_ALIAS)
        self.assertIsNotNone(room)
        self.assertIsInstance(room, ChatRoom)
        elapsed_time = time.perf_counter() - start_time
        log(f"[+] Completed create single ChatRoom instance in {elapsed_time:.5f}")

    def test_add_group_member(self):
        start_time = time.perf_counter()
        new_user = self.generate_random_string(5)
        room = ChatRoom(room_name=ROOM_NAME, room_type=ROOM_TYPE, owner_alias=OWNER_ALIAS)
        room.add_group_member(alias=new_user)
        self.assertIn(new_user, room.member_list)
        elapsed_time = time.perf_counter() - start_time
        log(f"[+] Completed add group member test in {elapsed_time:.5f}")

    def test_user_is_registered(self):
        start_time = time.perf_counter()
        new_user = self.generate_random_string(4)
        room = ChatRoom(room_name=ROOM_NAME, room_type=ROOM_TYPE, owner_alias=OWNER_ALIAS)
        room.add_group_member(alias=new_user)
        self.assertTrue(room.is_registered(new_user))
        elapsed_time = time.perf_counter() - start_time
        log(f"[+] Completed is registered test in {elapsed_time:.5f}")

    def test_unregistered_user(self):
        pass

class MessageTests(unittest.TestCase):
    """Test cases for sending and recieving messages through the chat room"""

    def setUp(self) -> None:
        return super().setUp()

    def test_send_single_message():
        pass

    def test_recieve_single_message():
        pass

    def test_send_100_messages():
        pass

    def test_recieve_all_messages():
        pass

    def test_recieve_100_messages():
        pass