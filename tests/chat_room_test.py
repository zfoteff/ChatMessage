"""Test suite for unit testing the Message Properties Class"""

__version__ = "1.0.0"
__author__ = "Zac Foteff"

from ast import Str
import unittest
import time
import string
import random
from bin.logger import Logger
from bin.constants import *
from src.chat_room import ChatRoom
from tests.api_test import FROM_ALIAS, TEST_MESSAGE, TO_ALIAS

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
        """Test that a single instance of a ChatRoom can be created"""
        start_time = time.perf_counter()
        room = ChatRoom(room_name=ROOM_NAME, room_type=ROOM_TYPE, owner_alias=OWNER_ALIAS)
        self.assertIsNotNone(room)
        self.assertIsInstance(room, ChatRoom)
        elapsed_time = time.perf_counter() - start_time
        log(f"[+] Completed create single ChatRoom instance in {elapsed_time:.5f}")

    def test_add_group_member(self):
        """Test that adding a member to the ChatRoom's member list """
        start_time = time.perf_counter()
        new_user = self.generate_random_string(5)
        room = ChatRoom(room_name=ROOM_NAME, room_type=ROOM_TYPE, owner_alias=OWNER_ALIAS)
        room.add_group_member(alias=new_user)
        self.assertIn(new_user, room.member_list)
        elapsed_time = time.perf_counter() - start_time
        log(f"[+] Completed add group member test in {elapsed_time:.5f}")

    def test_user_is_registered(self):
        """Test that a user can be registered to chatroom"""
        start_time = time.perf_counter()
        new_user = self.generate_random_string(4)
        room = ChatRoom(room_name=ROOM_NAME, room_type=ROOM_TYPE, owner_alias=OWNER_ALIAS)
        room.add_group_member(alias=new_user)
        self.assertTrue(room.is_registered(new_user))
        elapsed_time = time.perf_counter() - start_time
        log(f"[+] Completed is registered test in {elapsed_time:.5f}")

class MessageTests(unittest.TestCase):
    """Test cases for sending and recieving messages through the chat room"""

    def setUp(self) -> None:
        return super().setUp()

    def generate_random_string(self, length:int = 3) -> str:
        """Output a random string of letters 

        Args:
            length (int): Length of word to output
        Returns:
            str: Random word that is the specified length
        """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    def test_send_single_message(self):
        """"""
        start_time = time.perf_counter()
        room = ChatRoom(room_name=ROOM_NAME, room_type=ROOM_TYPE, owner_alias=OWNER_ALIAS)
        room.send_message(TEST_MESSAGE, ROOM_NAME, FROM_ALIAS, TO_ALIAS)
        self.assertIsNotNone(room.find_message(message_text=TEST_MESSAGE))
        self.assertIn(TEST_MESSAGE, room.get_messages())
        elapsed_time = time.perf_counter() - start_time
        log(f"[+] Completed send single message test in {elapsed_time}")

    def test_recieve_single_message(self):
        start_time = time.perf_counter()
        room = ChatRoom(room_name=ROOM_NAME, room_type=ROOM_TYPE, owner_alias=OWNER_ALIAS)
        messages = room.get_messages(num_messages=1)
        self.assertIsNotNone(messages)
        self.assertIsInstance(messages, list)
        self.assertEqual(len(messages), 1)
        elapsed_time = time.perf_counter() - start_time
        log(f"[+] Completed send single message test in {elapsed_time}")
    
    def test_recieve_all_messages(self):
        start_time = time.perf_counter()
        room = ChatRoom(room_name=ROOM_NAME, room_type=ROOM_TYPE, owner_alias=OWNER_ALIAS)
        messages = room.get_messages()
        self.assertEqual(len(messages), room.length)
        elapsed_time = time.perf_counter() - start_time
        log(f"[+] Completed send single message test in {elapsed_time}")

"""
WARNING: LONG
    def test_send_100_messages(self):
        start_time = time.perf_counter()
        room = ChatRoom(room_name=ROOM_NAME, room_type=ROOM_TYPE, owner_alias=OWNER_ALIAS)
        message_list = list()
        for counter in range(100):
            message = self.generate_random_string(5)
            message_list.append(message)
            room.send_message(message, ROOM_NAME, FROM_ALIAS, TO_ALIAS)
        
        retreived_messages = room.get_messages(num_messages=100)
        for message in message_list:
            self.assertIn(message, retreived_messages)
        room.get_messages()
        elapsed_time = time.perf_counter() - start_time
        log(f"[+] Completed send single message test in {elapsed_time}")
"""