"""Test suite for unittesting the Chat Message Class"""

__version__ = "1.0.0"
__author__ = "Zac Foteff"

import unittest
import time
from bin.logger import Logger
from bin.constants import *
from src.chat_message import ChatMessage
from src.message_props import MessageProperties

log = Logger("./chatMessageTest")


class ChatMessageTests(unittest.TestCase):
    """Test cases for ChatMessage class object"""

    TEST_ROOM = "zfoteff_test"
    TEST_MESSAGE = "Test message"
    TEST_MESSAGE_TYPE = "Cool"

    def setUp(self) -> None:
        return super().setUp()

    def test_create_single_instance(self):
        """
        Assert that a single instance can be created and contains the correct properties. 
        Depends on a MessageProperties object being instantiated
        """
        start_time = time.perf_counter()
        mess_prop = MessageProperties(0, 1, self.TEST_MESSAGE_TYPE, self.TEST_ROOM, "Zac in the future",
                                      "Zac in the past")
        chat_mess = ChatMessage(self.TEST_MESSAGE, mess_prop)
        self.assertIsNotNone(mess_prop)
        self.assertIsNotNone(chat_mess)
        self.assertIsInstance(chat_mess, ChatMessage)
        self.assertEqual(chat_mess.message, self.TEST_MESSAGE)
        self.assertEqual(chat_mess.mess_props, mess_prop)
        elapsed_time = time.perf_counter() - start_time
        log(chat_mess, 'd')
        log(chat_mess.to_dict(), 'd')
        log(f"[+] Completed create single instance test in {elapsed_time:.5f}")

    def test_instance_without_properties(self):
        """
        Assert that an instance of ChatMessage created without message properties autogenerates 
        the properties in the constructor. The message properties of the Chat message should not
        be None after creation and should contain mostly placeholder values
        """
        start_time = time.perf_counter()
        chat_mess = ChatMessage(self.TEST_MESSAGE)
        self.assertIsNotNone(chat_mess)
        self.assertIsNotNone(chat_mess.mess_props)
        self.assertEqual(chat_mess.message, self.TEST_MESSAGE)

        mess_props = chat_mess.mess_props.to_dict()
        self.assertEqual(mess_props['mess_type'], MESSAGE_SENT)
        self.assertEqual(mess_props['sequence_num'], -1)
        self.assertEqual(mess_props['from_user'], "Unknown")
        self.assertEqual(mess_props['to_user'], "Unknown"),
        self.assertEqual(mess_props['room_name'], "Auto generated properties"),
        elapsed_time = time.perf_counter() - start_time
        log(chat_mess, 'd')
        log(f"[+] Completed create instance without properties test in {elapsed_time:.5f}")

    def test_create_identical_instances(self):
        """
        Assert that two instances of the ChatMessage object with identical parameters create
        two seperate objects
        """
        start_time = time.perf_counter()
        mess_prop_1 = MessageProperties(MESSAGE_SENT, self.TEST_ROOM, "u1", 'u2')
        mess_prop_2 = MessageProperties(MESSAGE_SENT, self.TEST_ROOM, "u1", 'u2')
        chat_mess_1 = ChatMessage(self.TEST_MESSAGE, mess_prop_1)
        chat_mess_2 = ChatMessage(self.TEST_MESSAGE, mess_prop_2)
        self.assertIsNotNone(chat_mess_1)
        self.assertIsNotNone(chat_mess_2)
        self.assertIsInstance(chat_mess_1, ChatMessage)
        self.assertIsInstance(chat_mess_2, ChatMessage)
        self.assertIsNot(chat_mess_1, chat_mess_2)
        log(chat_mess_1, 'd')
        log(chat_mess_2, 'd')
        elapsed_time = time.perf_counter() - start_time
        log(f"[+] Completed identical instances test in {elapsed_time:.5f}")
