""" Test Suite for the Message Chat API
"""
__version__ = "1.0.0"
__author__ = "Zac Foteff"

import unittest
import time
from webbrowser import BackgroundBrowser
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
    QUERY_STRING = f"?room_name={TEST_ROOM}&message={TEST_MESSAGE}&from_alias={TEST_FROM_ALIAS}&to_alias={TEST_TO_ALIAS}"
    SEND_ROUTE = "/send/"
    SEND_SUCCESS_CODE = 200
    SEND_SUCCESS_MESSAGE = "ENQUEUED"

    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_send_single_message(self) -> None:
        start_time = time.perf_counter()
        response = self.client.get(URL+self.SEND_ROUTE+self.QUERY_STRING)
        response_message = response.json()
        print (response_message)
        self.assertEqual(response.status_code, self.SEND_SUCCESS_CODE)
        self.assertEqual(response_message["result"], "ENQUEUED")
        elapsed_time = time.perf_counter() - start_time
        log(f"Completed send message route test in {elapsed_time:.5f}")


class MessagesTestCases(unittest.TestCase):
    """Test suite for the recieve messages API route"""

    TEST_ROOM = "zfoteff_test"
    TEST_FROM_ALIAS = "t1"
    TEST_TO_ALIAS = "t2"
    MESSAGES_ROUTE = "/send/"
    MESSAGES_SUCCESS_CODE = 200

    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_recieve_from_empty_room(self) -> None:
        """Assert that the endpoint handles consuming from an empty RMQ"""
        start_time = time.perf_counter()
        response = self.client.get(URL)
        response_mesage = response.json()
        self.assertEqual(response.status_code, self.SEND_SUCCESS_CODE)
        self.assertEqual(response_mesage["result"], "ENQUEUED")
        elapsed_time = time.perf_counter() - start_time
        log(f"Completed send message route test in {elapsed_time:.5f}")