"""Test suite for unittesting the Message Properties Class"""
__version__ = "1.0.0"
__author__ = "Zac Foteff"

import unittest
import time
from bin.logger import Logger
from fastapi.testclient import TestClient
from message_props import MessageProperties

log = Logger("./messagePropertiesTest")

class MessagePropertiesTests(unittest.TestCase):
    """Test cases for MeessageProperties class object"""

    def setUp(self) -> None:
        return super().setUp()

    def test_create_single_instance():
        """Assert that a single instance can be created and contains the correct properties"""
        start_time = time.perf_counter()
        mess_prop = MessageProperties()
        elapsed_time = time.perf_counter() - start_time