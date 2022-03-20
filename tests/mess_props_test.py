"""Test suite for unittesting the Message Properties Class"""

__version__ = "1.0.0"
__author__ = "Zac Foteff"

import unittest
import time
from bin.logger import Logger
from message_props import MessageProperties

log = Logger("./messagePropertiesTest")

class MessagePropertiesTests(unittest.TestCase):
    """Test cases for MeessageProperties class object"""

    TEST_ROOM = "zfoteff_test"
    TEST_MESSAGE_TYPE = "Cool"

    def setUp(self) -> None:
        return super().setUp()

    def test_create_single_instance(self):
        """Assert that a single instance can be created and contains the correct properties"""
        start_time = time.perf_counter()
        mess_prop = MessageProperties(0, 1, self.TEST_MESSAGE_TYPE, self.TEST_ROOM, "Zac in the future", "Zac in the past")
        self.assertIsNotNone(mess_prop)
        self.assertEqual(mess_prop.message_type, self.TEST_MESSAGE_TYPE)
        self.assertEqual(mess_prop.room_name, self.TEST_ROOM)
        log(mess_prop, 'd')
        log(mess_prop.to_dict(), 'd')
        elapsed_time = time.perf_counter() - start_time
        log(f"Completed create single instance test in {elapsed_time:.5f}")