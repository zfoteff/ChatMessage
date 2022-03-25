"""
RabbitMQ interaction helper file
"""
__author__ = "Zac Foteff"
__version__ = "2.0.0."

import pika
from bin.logger import Logger
from bin.constants import *

log = Logger(key="messageServer")

class RMQMessageInteractions:
    """
    Rabbit Message Queue interaction object
    """
    def __init__(self, 
                host=RMQ_PROD_HOST, 
                queue: str=RMQ_DEFAULT_PUBLIC_QUEUE, 
                exchange: str=RMQ_DEFAULT_PUBLIC_EXCHANGE):
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
        self.__exchange_name = exchange
        self.__exchange = None
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
    def exchange(self):
        return self.__exchange

    @property
    def exchange_name(self):
        return self.__exchange_name
    
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

    def declare_exchange(self, exchange_name: str, exchange_type: str=RMQ_DEFAULT_EXCHANGE_TYPE) -> None:
        """Declare an exchange and bind it to the current queue being consumed

        Args:
            exchange_name (str): Name for the exchange
            exchange_type (str, optional): RMQ type for the exchange. Defaults to 'fanout'.
        """
        self.__exchange = self.channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)
        self.channel.queue_bind(exchange=exchange_name, queue=self.queue)

class RMQProperties:
    """
    RabbitMQ properties container object
    """
    def __init__(self, index, name, consumer_tag, delivery_tag, exchange, redelivered, routing_key, synchronous, app_id, cluster_id,
    content_encoding, content_type, correlation_id, delivery_mode, expiration, headers, message_id, priority, reply_to, timestamp, type, user_id) -> None:
        self.index = index
        self.name = name
        self.consumer_tag = consumer_tag
        self.delivery_tag = delivery_tag
        self.exchange = exchange
        self.redelivered = redelivered
        self.routing_key = routing_key
        self.synchrous = synchronous
        self.app_id = app_id
        self.cluster_id = cluster_id
        self.content_encoding = content_encoding
        self.content_type = content_type
        self.correlation_id = correlation_id
        self.delivery_mode = delivery_mode
        self.expiration = expiration
        self.headers = headers
        self. message_id = message_id
        self.priority = priority
        self.reply_to = reply_to
        self.timestamp = timestamp
        self.type = type
        self.user_id = user_id

    def to_dict(self):
        return {
            "index": self.index,
            "name": self.name,
            "consumer_tag": self.consumer_tag,
            "delivery_tag": self.delivery_tag,
            "exchange": self.exchange,
            "redelivered": self.redelivered,
            "routing_key": self.routing_key,
            "synchrous": self.synchronous,
            "app_id": self.app_id,
            "cluster_id": self.cluster_id,
            "content_encoding": self.content_encoding,
            "content_type": self.content_type,
            "correlation_id": self.correlation_id,
            "delivery_mode":self.delivery_mode,
            "expiration": self.expiration,
            "headers": self.headers,
            "message_id": self.message_id,
            "priority": self.priority,
            "reply_to": self.reply_to,
            "timestamp": self.timestamp,
            "type": self.type,
            'user_id': self.user_id,
        }