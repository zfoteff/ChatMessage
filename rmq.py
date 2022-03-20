"""
RabbitMQ interaction helper file
"""
__author__ = "Zac Foteff"
__version__ = "2.0.0."

import pika
from bin.logger import Logger
from chat_message import ChatMessage
from bin.constants import *

log = Logger(key="messageServer")

class RMQMessageInteractions:
    """
    Rabbit Message Queue interaction object
    """
    def __init__(self, host=RMQ_PROD_HOST, queue: str=RMQ_DEFAULT_PUBLIC_QUEUE):
        """
        Instantiate RabbitMQ interaction interface. Allows user to pass a queue to connect to. Will create
        a connection to the RMQ server that allows user to send and recieve messages. Depends on the 
        ChatMessage class

        Args:
            queue (str, optional): Queue to connect to for sending and recieving messages. 
            Defaults to RMQ_DEFAULT_PUBLIC_QUEUE.
        """
        self.__host = host
        self.__queue = queue
        self.__creds = pika.PlainCredentials(RMQ_USER, RMQ_PASS)
        self.__params = pika.ConnectionParameters(host, RMQ_PORT, "/", self.__creds)
        self.__connection = pika.BlockingConnection(self.__params)
        self.__channel = self.__connection.channel()
        self.__channel.queue_declare(self.__queue)
        log("[-+-] Connected to RMQ server")

    @property
    def queue(self) -> str:
        return self.__queue

    @property
    def host(self) -> str:
        return self.__host

    @property
    def channel(self):
        return self.__channel
    
    @property
    def connection(self):
        return self.__connection
            
    def close(self) -> None:
        """
        Close active channel and connection to RMQ server
        """
        self.__channel.cancel()
        self.__channel.close()
        self.__connection.close()
        log("[-X-] Disconnected from RMQ server")
        
    def sendMessage(self, message: ChatMessage) -> dict:
        """
        Send message to the RMQ server. Once the message is published, it should return a 
        message stating the operation was successful

        Args:
            message (str): ChatMessage to send to RMQ
        Returns:
            dict: Result message
        """
        try:
            message = message.encode('utf-8')
            self.__channel.basic_publish(exchange='', body=message.message, routing_key=self.__queue)
            log(f"[+] Published messsage to queue {self.__queue}")
            return {"result": "ENQUEUED"}
        except:
            return {"result": "MESSAGE DROPPED"}
    
    def recieveMessages(self, num_messages: int=GET_ALL_MESSAGES) -> dict:
        """
        Recieve messages from the server. The method provides an option to try and retrieve 
        a specific number of messages, or retrieve all messages

        Args:
            num_messages (int, optional): Number of messages to retrieve from the server. 
            Defaults to GET_ALL_MESSAGES.

        Returns:
            dict: Indexed dictionary of messages. Resembles a JSON object so it can 
            be displayed in a browser
        """
        log(f"[*] Started consuming messages all messages from queue '{self.__queue}'")
        chat_messages = {}
        counter = 0
        while True:
            try:   
                if counter == num_messages:
                    break
                
                _, _, body = self.__channel.basic_get(self.__queue, auto_ack=True)
                if body == None:
                    log(f"[-] Consumed all {counter} available messages in the queue")
                    break
                
                counter += 1 
                log(f"[-] Consumed message: {body}")
                chat_messages[counter] = body.decode('utf-8')
            except:
                log("Error consuming messages", 'e')
                break
        
        log(f"[*] Finished consuming messages")
        return chat_messages