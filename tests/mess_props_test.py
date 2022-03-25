"""Test suite for unittesting the Message Properties Class"""

__version__ = "1.0.0"
__author__ = "Zac Foteff"

import unittest
import time
from bin.logger import Logger
from bin.constants import *
from src.message_props import MessageProperties

log = Logger("./messagePropertiesTest")

class MessagePropertiesTests(unittest.TestCase):
    """Test cases for MeessageProperties class object"""

    TEST_ROOM = "zfoteff_test"

    def setUp(self) -> None:
        return super().setUp()

    def test_create_single_instance(self):
        """Assert that a single instance can be created and contains the correct properties"""
        start_time = time.perf_counter()
        mess_prop = MessageProperties(MESSAGE_SENT, self.TEST_ROOM, "Zac in the future", "Zac in the past")
        self.assertIsNotNone(mess_prop)
        self.assertIsInstance(mess_prop, MessageProperties)
        self.assertEqual(mess_prop.mess_type, MESSAGE_SENT)
        self.assertEqual(mess_prop.room_name, self.TEST_ROOM)
        log(mess_prop, 'd')
        log(mess_prop.to_dict(), 'd')
        elapsed_time = time.perf_counter() - start_time
        log(f"[+] Completed create single instance test in {elapsed_time:.5f}")

    def test_create_identical_instances(self):
        """Assert that multiple instances with the same parameters create new objects"""
        start_time = time.perf_counter()
        mess_prop_1 = MessageProperties(MESSAGE_SENT, self.TEST_ROOM, "u1", 'u2')
        mess_prop_2 = MessageProperties(MESSAGE_SENT, self.TEST_ROOM, "u1", 'u2')
        self.assertIsNotNone(mess_prop_1)
        self.assertIsNotNone(mess_prop_2)
        self.assertIsInstance(mess_prop_1, MessageProperties)
        self.assertIsInstance(mess_prop_2, MessageProperties)
        self.assertIsNot(mess_prop_1, mess_prop_2)
        log(mess_prop_1, 'd')
        log(mess_prop_2, 'd')
        elapsed_time = time.perf_counter() - start_time
        log(f"[+] Completed identical instances test in {elapsed_time:.5f}")