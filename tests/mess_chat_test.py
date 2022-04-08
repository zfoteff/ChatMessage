""" Test Suite for the Message Chat API
"""
__version__ = "1.0.0"
__author__ = "Zac Foteff"

import unittest
import time
from bin.logger import Logger
from fastapi.testclient import TestClient
from room_chat_api import app

URL = 'http://localhost:8000/'
log = Logger("./messageServerTest")


class SuccessfulConnectionTestCases(unittest.TestCase):
    """Test suite for the message chat application API connection tests"""

    SUCCESS_CODE = 200

    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_successful_connection(self):
        """Assert that the website is up"""
        start_time = time.perf_counter()
        response = self.client.get(URL)
        self.assertEqual(response.status_code, self.SUCCESS_CODE)
        elapsed_time = time.perf_counter() - start_time
        log(f"Completed GET root test in {elapsed_time}")


class SendTestCases(unittest.TestCase):
    """Test suite for the send message API route"""

    TEST_ROOM = "zfoteff_test"
    TEST_MESSAGE = "TEST MESSAGE FOR CONSUMPTION"
    TEST_FROM_ALIAS = "t1"
    TEST_TO_ALIAS = "t2"
    QUERY_STRING = f"?message={TEST_MESSAGE}&room_name={TEST_ROOM}&from_alias={TEST_FROM_ALIAS}&to_alias={TEST_TO_ALIAS}"
    SEND_ROUTE = "/message/"
    SEND_SUCCESS_CODE = 201
    SEND_SUCCESS_MESSAGE = "Enqueued message"

    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_send_single_message(self) -> None:
        start_time = time.perf_counter()
        response = self.client.post(self.SEND_ROUTE + self.QUERY_STRING)
        self.assertEqual(response.status_code, self.SEND_SUCCESS_CODE)
        self.assertEqual(response.json(), self.SEND_SUCCESS_MESSAGE)
        elapsed_time = time.perf_counter() - start_time
        log(f"Completed send message route test in {elapsed_time:.5f}")


class MessagesTestCases(unittest.TestCase):
    """Test suite for the receiving messages API route"""

    TEST_ROOM = "zfoteff_test"
    TEST_FROM_ALIAS = "t1"
    TEST_TO_ALIAS = "t2"
    MESSAGES_ROUTE = "/send/"
    MESSAGES_SUCCESS_CODE = 200

    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_recieve_from_room(self) -> None:
        """Assert that the endpoint handles consuming from an ChatRoom"""
        start_time = time.perf_counter()

        elapsed_time = time.perf_counter() - start_time
        log(f"Completed send message route test in {elapsed_time:.5f}")


class RegisterUserTestCases(unittest.TestCase):
    """Test suite for registering a user to the application user list"""

    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_register_user(self):
        """Assert that the endpoint handles consuming from an empty RMQ"""
        start_time = time.perf_counter()

        elapsed_time = time.perf_counter() - start_time
        log(f"Completed send message route test in {elapsed_time:.5f}")
