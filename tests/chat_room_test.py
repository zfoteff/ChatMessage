"""Test suite for unit testing the Message Properties Class"""

__version__ = "1.0.0"
__author__ = "Zac Foteff"

import unittest
import time
import string
import random
from bin.logger import Logger
from bin.constants import *
from src.chat_message import ChatMessage
from src.chat_room import ChatRoom

log = Logger("./chatRoomTest")
ROOM_NAME = "zfoteff_chatroom_tests"
PUBLIC_ROOM_TYPE = CHAT_ROOM_TYPE_PUBLIC
PRIVATE_ROOM_TYPE = CHAT_ROOM_TYPE_PRIVATE
OWNER_ALIAS = 'zfoteff'
FROM_ALIAS = "Alice"
TO_ALIAS = "Bob"
BLOCKED_ALIAS = 'Eve'

class ChatRoomTests(unittest.TestCase):
    """Test cases for ChatRoom class object"""

    def setUp(self) -> None:
        return super().setUp()

    def generate_random_string(self, length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    def test_create_single_instance(self):
        """Test that a single instance of a ChatRoom can be created"""
        start_time = time.perf_counter()
        room = ChatRoom(room_name=ROOM_NAME, room_type=PUBLIC_ROOM_TYPE, owner_alias=OWNER_ALIAS)
        self.assertIsNotNone(room)
        self.assertIsInstance(room, ChatRoom)
        elapsed_time = time.perf_counter() - start_time
        log(f"[+] Completed create single ChatRoom instance in {elapsed_time:.5f} seconds")

    def test_add_group_member(self):
        """Test that adding a member to the ChatRoom's member list """
        start_time = time.perf_counter()
        new_user = self.generate_random_string(5)
        room = ChatRoom(room_name=ROOM_NAME, room_type=PUBLIC_ROOM_TYPE, owner_alias=OWNER_ALIAS)
        register_result = room.register_group_member(alias=new_user)
        self.assertTrue(register_result)
        self.assertIn(new_user, room.member_list.get_all_users())
        elapsed_time = time.perf_counter() - start_time
        log(f"[+] Completed add group member test in {elapsed_time:.5f} seconds")

    def test_user_is_registered(self):
        """Test that a user can be registered to chatroom"""
        start_time = time.perf_counter()
        new_user = self.generate_random_string(4)
        room = ChatRoom(room_name=ROOM_NAME, room_type=PUBLIC_ROOM_TYPE, owner_alias=OWNER_ALIAS)
        room.register_group_member(alias=new_user)
        self.assertTrue(room.get_group_member(new_user))
        elapsed_time = time.perf_counter() - start_time
        log(f"[+] Completed is registered test in {elapsed_time:.5f} seconds")

    def test_restore_chatroom(self):
        """Test that ChatRoom instances can be successfully restored from MongoDB"""
        RAND_ROOM_NAME = self.generate_random_string(10)
        start_time = time.perf_counter()
        room = ChatRoom(room_name=RAND_ROOM_NAME, room_type=PUBLIC_ROOM_TYPE, owner_alias=OWNER_ALIAS)
        original_room_metadata = room.metadata()
        room = None
        new_room = ChatRoom(room_name=RAND_ROOM_NAME, room_type=PUBLIC_ROOM_TYPE, owner_alias=OWNER_ALIAS)
        new_room_metadata = new_room.metadata()
        self.assertIsNone(room)
        self.assertIsNotNone(new_room)
        self.assertEqual(new_room_metadata, original_room_metadata)
        elapsed_time = time.perf_counter() - start_time
        log(f"[+] Completed restore ChatRoom instance test in {elapsed_time:.5f} seconds")

    def test_restore_messages(self):
        """Test that all messages in the ChatRoom obj are successfully restored from MongoDB"""
        messages_to_send = [
            "restored message 1",
            "restored message 2",
            "restored message 3",
            "restored message 4",
            "restored message 5",
        ]
        RAND_ROOM_NAME = self.generate_random_string(10)
        start_time = time.perf_counter()
        room = ChatRoom(room_name=RAND_ROOM_NAME, room_type=PUBLIC_ROOM_TYPE, owner_alias=OWNER_ALIAS)
        room_metadata = room.metadata()
        for message in messages_to_send:
            room.send_message(message, TO_ALIAS, FROM_ALIAS)
        room_messages = room.get_messages(TO_ALIAS)
        room = None
        new_room = ChatRoom(room_name=RAND_ROOM_NAME, room_type=PUBLIC_ROOM_TYPE, owner_alias=OWNER_ALIAS)
        new_room_messages = new_room.get_messages(TO_ALIAS)
        self.assertIsNone(room)
        self.assertIsNotNone(new_room)
        self.assertEqual(room_messages, new_room_messages)
        for message in new_room.get_messages(TO_ALIAS):
            self.assertIn(message, messages_to_send)
        elapsed_time = time.perf_counter() - start_time
        log(f"[+] Completed restore ChatRoom messages test in {elapsed_time:.5f} seconds")

    def test_restore_userlist(self):
        """Test that the UserList obj contained in the ChatRoom obj is successfully restored from MongoDB"""
        start_time = time.perf_counter()

        elapsed_time = time.perf_counter() - start_time
        log(f"[+] Completed restore ChatRoom user list test in {elapsed_time:.5f} seconds")

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
        """Test that the application behaves correctly when sending a single message"""
        start_time = time.perf_counter()
        TEST_MESSAGE = "send single message test"
        room = ChatRoom(room_name=ROOM_NAME, room_type=PUBLIC_ROOM_TYPE, owner_alias=OWNER_ALIAS)
        room.register_group_member(TO_ALIAS)
        room.register_group_member(FROM_ALIAS)
        room.send_message(message=TEST_MESSAGE, from_alias=FROM_ALIAS, to_alias=TO_ALIAS)
        self.assertIn(TO_ALIAS, room.member_list.get_all_users())
        self.assertIn(FROM_ALIAS, room.member_list.get_all_users())
        self.assertIsNotNone(room.find_message(message_text=TEST_MESSAGE))
        self.assertIn(TEST_MESSAGE, room.get_messages(TO_ALIAS))
        elapsed_time = time.perf_counter() - start_time
        log(f"[+] Completed send single message test in {elapsed_time:.5f} seconds")

    def test_recieve_single_message(self):
        start_time = time.perf_counter()
        room = ChatRoom(room_name=ROOM_NAME, room_type=PUBLIC_ROOM_TYPE, owner_alias=OWNER_ALIAS)
        print(room.member_list.to_dict())
        messages = room.get_messages(alias=TO_ALIAS, num_messages=1)
        self.assertIsNotNone(messages)
        self.assertIsInstance(messages, list)
        self.assertEqual(len(messages), 1)
        elapsed_time = time.perf_counter() - start_time
        log(f"[+] Completed send single message test in {elapsed_time:.5f} seconds")
    
    def test_recieve_all_messages(self):
        start_time = time.perf_counter()
        room = ChatRoom(room_name=ROOM_NAME, room_type=PUBLIC_ROOM_TYPE, owner_alias=OWNER_ALIAS)
        messages = room.get_messages()
        self.assertEqual(len(messages), room.length)
        elapsed_time = time.perf_counter() - start_time
        log(f"[+] Completed send single message test in {elapsed_time}")

    def test_recieve_all_messages_as_objects(self):
        start_time = time.perf_counter()
        room = ChatRoom(room_name=ROOM_NAME, room_type=PUBLIC_ROOM_TYPE, owner_alias=OWNER_ALIAS)
        message_objects = room.get_messages(alias=TO_ALIAS, return_objects=True)
        self.assertEqual(len(message_objects), room.length)
        for message in message_objects:
            self.assertIsInstance(message, ChatMessage)
        elapsed_time = time.perf_counter() - start_time
        log(f"[+] Completed recieve all messages as ChatMessage objects test in {elapsed_time:.5f} seconds")

"""
WARNING: LONG
    def test_send_100_messages(self):
        start_time = time.perf_counter()
        room = ChatRoom(room_name=ROOM_NAME, room_type=ROOM_TYPE, owner_alias=OWNER_ALIAS)
        message_list = list()
        for counter in range(100):
            message = self.generate_random_string(5)
            message_list.append(message)
            room.send_message(message, FROM_ALIAS, TO_ALIAS)
        
        retreived_messages = room.get_messages(num_messages=100)
        for message in message_list:
            self.assertIn(message, retreived_messages)
        room.get_messages()
        elapsed_time = time.perf_counter() - start_time
        log(f"[+] Completed send single message test in {elapsed_time}")
"""