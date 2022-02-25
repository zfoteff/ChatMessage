import pika
from bin.logger import Logger

RMQ_DEV_HOST = "localhost"
RMQ_PROD_HOST = "35.236.51.203"
RMQ_PORT = 5672
EXCHANGE_TYPE = "fanout"
RMQ_USER = "class"
RMQ_PASS = "CPSC313"
RMQ_DEFAULT_PUBLIC_QUEUE = "general"
RMQ_PRIVATE_QUEUE = "foteff"
DB_HOST = '34.94.157.136'
DB_PORT = '5672'
GET_ALL_MESSAGES = -1

logger = Logger(key="messageServer")

class RMQMessageInteractions:
    """
    Rabbit Message Queue interaction object
    """
    def __init__(self, host=RMQ_PROD_HOST, queue: str=RMQ_DEFAULT_PUBLIC_QUEUE):
        """
        Instantiate manipulation object. Allows user to pass a queue to connect to. Will create
        a connection to the RMQ server that allows user to send and recieve messages

        Args:
            queue (str, optional): Queue to connect to for sending and recieving messages. 
            Defaults to RMQ_DEFAULT_PUBLIC_QUEUE.
        """
        self._creds = pika.PlainCredentials(RMQ_USER, RMQ_PASS)
        self._params = pika.ConnectionParameters(host, RMQ_PORT, "/", self._creds)
        self._queue = queue
        self._connection = pika.BlockingConnection(self._params)
        self._channel = self._connection.channel()
        self._channel.queue_declare(self._queue)
        logger("[-+-] Connected to RMQ server")
            
    def close(self):
        """
        Close active channel and connection to RMQ server
        """
        self._channel.cancel()
        self._channel.close()
        self._connection.close()
        logger("[-X-] Disconnected from RMQ server")
        
    def sendMessage(self, message: str):
        """
        Send message to the RMQ server. Once the message is published, it should return a 
        message stating the operation was successful

        Args:
            message (str): Message to send to RMQ
        Returns:
            dict: Result message
        """
        try:
            message = message.encode('utf-8')
            self._channel.basic_publish(exchange='', body=message, routing_key=self._queue)
            logger(f"[+] Published messsage to queue {self._queue}")
            return {"result": "ENQUEUED"}
        except:
            return {"result": "MESSAGE DROPPED"}
    
    def recieveMessages(self, num_messages: int=GET_ALL_MESSAGES):
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
        logger(f"[*] Started consuming messages all messages from queue '{self._queue}'")
        chat_messages = {}
        counter = 0
        while True:
            try:   
                if counter == num_messages:
                    break
                
                _, _, body = self._channel.basic_get(self._queue, auto_ack=True)
                
                if body == None:
                    logger(f"[-] Consumed all {counter} available messages in the queue")
                    break
                
                counter += 1 
                logger(f"[-] Consumed message: {body}")
                chat_messages[counter] = body.decode('utf-8')
            except:
                logger("Error consuming all messages")
                break
        
        logger(f"[*] Finished consuming messages")
        return chat_messages

    @property
    def channel(self):
        return self._channel
    
    @property
    def queue(self):
        return self._queue
    
    @property
    def connection(self):
        return self._connection