import random
import string
import unittest
import time
from bin.logger import Logger
from bin.constants import *
from room_chat_api import app
from fastapi.testclient import TestClient

OWNER_ALIAS = "zfoteff"
ROOM_NAME = "zfoteff_test"
TO_ALIAS = "zfoteff_to"
FROM_ALIAS = "zfoteff_from"
TEST_MESSAGE = "zac's test message"
ROOM_TYPE = CHAT_ROOM_TYPE_PUBLIC
log = Logger("./apiTest")

class APITests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
        return super().setUp()

    def generate_random_string(self, length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    def test_create_room_route(self):
        start_time = time.perf_counter()
        new_room_name = self.generate_random_string(5)
        room_route_query_string = f"?room_name={new_room_name}&owner_alias={OWNER_ALIAS}"
        response = self.client.post("/room/"+room_route_query_string)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), "Successfully created new room")
        elapsed_time = time.perf_counter() - start_time
        log(f"[+] Completed create room route test in {elapsed_time:.5f}")

    def test_send_message_route(self):
        start_time = time.perf_counter()
        send_message_query_string = f"?room_name={ROOM_NAME}&message={TEST_MESSAGE}&from_alias={FROM_ALIAS}&to_alias={TO_ALIAS}"
        response = self.client.post("/message/"+send_message_query_string)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), "Enqueued message")
        elapsed_time = time.perf_counter() - start_time
        log(f"[+] Completed send message route test in {elapsed_time:.5f}")


    def test_get_messages_route(self):
        start_time = time.perf_counter()
        get_message_query_string = f"?alias={TO_ALIAS}&room_name={ROOM_NAME}"
        response = self.client.get("/messages/"+get_message_query_string)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        elapsed_time = time.perf_counter() - start_time
        log(f"[+] Completed get messages route test in {elapsed_time:.5f}")

    def test_get_users_route(self):
        start_time = time.perf_counter()
        response = self.client.get("/users/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        elapsed_time = time.perf_counter() - start_time
        log(f"[+] Completed get users route test in {elapsed_time:.5f}")

    def test_register_user_route(self):
        start_time = time.perf_counter()
        new_user = self.generate_random_string(5)
        register_user_query_string = f"?user_alias={new_user}"
        response = self.client.post("/register/user/"+register_user_query_string)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), "Success")
        elapsed_time = time.perf_counter() - start_time
        log(f"[+] Completed register user route test in {elapsed_time:.5f}")

    def test_register_then_get(self):
        start_time = time.perf_counter()
        new_user = self.generate_random_string(5)
        register_query_string = f"?user_alias={new_user}"
        register_response = self.client.post("/register/user/"+register_query_string)
        self.assertEqual(register_response.status_code, 201)
        get_response = self.client.get("/users/")
        self.assertEqual(get_response.status_code, 200)
        self.assertIn(new_user, get_response.json())
        elapsed_time = time.perf_counter() - start_time
        log(f"[+] Completed register user, then get user test in {elapsed_time:.5f}")

    def test_send_then_get(self):
        pass
