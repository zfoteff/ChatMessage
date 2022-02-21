from logger import Logger
from rmq import RMQ_PRIVATE_QUEUE, RMQMessageInteractions as RMQ
import time

URL = "http://localhost:8000/"
logger = Logger("rmqTests")

def test_successful_connection():
    """
    Test that RMQ server channel is opened when a new Server instance is created
    """
    start_time = time.perf_counter()
    rmq = RMQ()
    assert rmq.channel.is_open
    elapsed_time = time.perf_counter() - start_time
    logger(f"Completed connection test in {elapsed_time:.5f} seconds")
    rmq.close()
    
def test_produce_single_message():
    """
    Test that a single message can be successfully enqueued in the RMQ server
    """
    start_time = time.perf_counter()
    rmq = RMQ()
    test_message = "test produce single message"
    result = rmq.sendMessage(test_message)
    assert result["result"] == "ENQUEUED"
    elapsed_time = time.perf_counter() - start_time
    logger(f"Completed produce single message test in {elapsed_time:.5f} seconds")
    rmq.close()
    
def test_consume_single_message():
    """
    Test that a single message can be successfully consumed by the RMQ server
    """
    rmq = RMQ()
    test_message = "Do I exist?"
    start_time = time.perf_counter()
    rmq.sendMessage(test_message)
    retrieved_chats = rmq.recieveMessages(5)
    assert test_message in retrieved_chats.values()
    elapsed_time = time.perf_counter() - start_time
    logger(f"Completed consume single message test in {elapsed_time:.5f} seconds")
    rmq.close()
    
def test_produce_multiple_messages():
    """
    Test that multiple messages can be produced at once by the RMQ server
    """
    rmq = RMQ()
    test_messages = ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8']
    start_time = time.perf_counter()
    for message in test_messages:
        result = rmq.sendMessage(message)
        assert result["result"] == "ENQUEUED"
    elapsed_time = time.perf_counter() - start_time
    logger(f"Completed produce multiple messages in {elapsed_time:.5f}")
    rmq.close()
    
def test_consume_multiple_messages():
    """
    Test that multiple messages can be consumed at once b the RMQ server
    """
    rmq = RMQ()
    test_messages = ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8']
    start_time = time.perf_counter()
    for message in test_messages:
        rmq.sendMessage(message)
    retrieved_messages = rmq.recieveMessages(10)
    for message in test_messages:
        assert message in retrieved_messages.values()
    elapsed_time = time.perf_counter() - start_time
    logger(f"Completed consume multiple messages in {elapsed_time:.5f}")
    rmq.close()
    
def test_connection_to_private_channel():
    """
    Test that RMQ server can connect to private queue
    """
    start_time = time.perf_counter()
    rmq = RMQ(RMQ_PRIVATE_QUEUE)
    assert rmq.channel.is_open
    elapsed_time = time.perf_counter() - start_time
    logger(f"Completed connection test in {elapsed_time:.5f} seconds")
    rmq.close()
    
def test_publish_to_private_channel():
    """
    Test that RMQ server can connect to private queue
    """
    start_time = time.perf_counter()
    test_message = "Test message for my private channel. Go Away!"
    rmq = RMQ(RMQ_PRIVATE_QUEUE)
    result = rmq.sendMessage(test_message)
    assert result["result"] == "ENQUEUED"
    elapsed_time = time.perf_counter() - start_time
    logger(f"Completed connection test in {elapsed_time:.5f} seconds")
    rmq.close()
    
def test_consume_from_private_channel():
    """
    Test that RMQ server can connect to private queue
    """
    start_time = time.perf_counter()
    rmq = RMQ(RMQ_PRIVATE_QUEUE)
    test_message = "Test message for my private channel. Go Away!"
    rmq.sendMessage(test_message)
    recieved_messages = rmq.recieveMessages()
    assert len(recieved_messages) == 1
    assert recieved_messages[1] == test_message
    elapsed_time = time.perf_counter() - start_time
    logger(f"Completed connection test in {elapsed_time:.5f} seconds")
    rmq.close()
    
def test_consume_all_from_private_channel():
    """
    Test that RMQ server can retrieval all stored messages in a queue
    """
    start_time = time.perf_counter()
    rmq = RMQ(RMQ_PRIVATE_QUEUE)
    test_messages = ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8']
    for message in test_messages:
        rmq.sendMessage(message)
    recieved_messages = rmq.recieveMessages()
    assert len(recieved_messages.keys()) == 8
    for message in test_messages:
        assert message in recieved_messages.values()
    elapsed_time = time.perf_counter() - start_time
    logger(f"Completed connection test in {elapsed_time:.5f} seconds")
    rmq.close()