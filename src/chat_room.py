"""
Class for interactions with MongoDB and RabbitMQ to create a Chat Room instance
"""

__author__ = "Zac Foteff"
__version__ = "1.0.0."

import pika
import pika.exceptions
from datetime import datetime
from pymongo import MongoClient, ReturnDocument
from collections import deque
from bin.logger import Logger
from src.message_props import MessageProperties
from src.chat_message import ChatMessage
from bin.constants import *

log = Logger("chatRoom")

class ChatRoom(deque):
    def __init__(
        self, 
        room_name: str=RMQ_DEFAULT_PUBLIC_QUEUE,
        room_type: int=CHAT_ROOM_TYPE_PUBLIC,
        member_list: list=[],
        owner_alias: str="",
        create_time: datetime=datetime.now(),
        modify_time: datetime=datetime.now()):
        """Intantiate a ChatRoom class object. All properties are created in the constructor, or
        restored from an existing entry in storage
        storage

        Args:
            room_name (str): Room name. Default queue_name for consuming is using message queues
            member_list (list): List of all registered members to the chatroom
            owner_alias (str): Alias of the room creator
            room_type (int, optional): Type of room. Defaults to public
            create_new (bool, optional): Flag indicating if the chat room exists in the database 
            create_time (datetime, optional): Time that the room was created
            modify_time (datetime, optional): Last time that the room was modified
        """
        super(ChatRoom, self).__init__()
        self.__room_name = room_name

        #   Initialize MongoDB resources
        self.__mongo_client = MongoClient(DB_HOST, DB_PORT)
        self.__mongo_db = self.__mongo_client.gufoteff
        self.__mongo_collection = self.__mongo_db.get_collection(room_name)
        if self.__mongo_collection is None:
            #   Initialize the chat queue collection in the DB if it does not already exist
            self.__mongo_collection = self.__mongo_db.create_collection(room_name)

        self.__mongo_seq_collection = self.__mongo_db.get_collection('sequence')
        if self.__mongo_seq_collection is None:
            #   Initialize the sequence number collection in the DB if it does not already exist
            self.__mongo_seq_collection = self.__mongo_db.create_collection('sequence')
            
        if self.__restore() is True:
            #   Element is restored from storage, so indicate there are no changes to be saved
            self.__dirty = False
        else:
            #   Element has not be restored, so a new Chat room is created
            self.__member_list = member_list
            self.__owner_alias = owner_alias
            self.__room_type = room_type
            self.__dirty = True
            self.__create_time = create_time
            self.__modify_time = modify_time

    @property
    def room_name(self):
        return self.__room_name

    @property
    def dirty(self):
        return self.__dirty

    @property
    def room_type(self) -> int:
        return self.__room

    @property
    def owner_alias(self) -> str:
        return self.__owner_alias

    @property
    def member_list(self):
        return self.__member_list

    @property
    def length(self) -> int:
        return len(self)

    def __persist(self):
        """Persist object data in MongoDB. First, save the user list if it isn't already there
        or there are changes that need to be persisted. Next, for each message in the list create
        and save a document for that user
        """
        if self.__mongo_collection.find_one({ 'room_name': { '$exists': 'false'}}) is None:
            self.__mongo_collection._insert_one({
                "room_name": self.room_name, 
                "create_time": self.__create_time, 
                "modify_time": self.__modify_time
                })
        
        for message in list(self):
            if message.dirty:
                serialized = message.to_dict()
                self.mongo_collection.insert_one(serialized)
                message.dirty = False

    def __restore(self):
        """Restore object data from MongoDB. Find record using the room name as a key and
        populate name, create, and modify time.
        Next, retrieve that messages associated with the chat room (every document with 
        a key called 'message'). For each dictionary we get back (the documents), create 
        a message properties instance and a message instance and put them in the deque by 
        calling the put method

        Returns:
            bool: Returns True if the object and its messages were restored successfully. 
            False otherwise
        """
        metadata = self.mongo_collection.find_one({'name': {'$exists': 'true'}})
        if metadata is None:
            log("[*] No metadata found for ChatRoom object", 'w')
            return False
        self.__room_name = metadata['room_name']
        self.__create_time = metadata['create_time']
        self.__modify_time = metadata['modify_time']
        for mess_dict in self.mongo_collection.find({'message': {'$exists': 'true'}}):
            new_mess_props = MessageProperties(
                mess_dict['mess_props']['mess_type'],
                mess_dict['mess_props']['room_name'],
                mess_dict['mess_props']['to_user'],
                mess_dict['mess_props']['from_user'],
                mess_dict['mess_props']['sequence_num'],
                mess_dict['mess_props']['sent_time'],
                mess_dict['mess_props']['rec_time'])
            new_message = ChatMessage(mess_dict['message'], new_mess_props, dirty=False)
            self.put(new_message)
        return True

    def __get_next_sequence_num(self) -> int:
        """Queries the sequence number collection from MongoDB and selects the next 
        sequence number to assign to the message

        Returns:
            int: Next sequence number to assign to new messages
        """
        sequence_num = self.__mongo_seq_collection.find_one_and_update(
            {'_id': 'userid'},
            {'$inc': {self.room_name: 1}},
            project={self.room_name: True, '_id': False},
            upsert=True,
            return_document=ReturnDocument.AFTER)
        return sequence_num

    def is_registered(self, username: str) -> bool:
        """Check if the inputted username is registered to the ChatRoom

        Args:
            username (str): Name to check the existance of
        Returns:
            bool: Return true if the name exists in the member list, false otherwise
        """
        return username in self.member_list

    def add_group_member(self, alias) -> bool:
        """Register new user to the room's whitelist. Takes an alias and returns True if
        the user isn't registered to the room and they were successfully added. Will return False
        if the user was already registered in the room, or an error prevents them from being added

        Args:
            alias (str): Alias of the user to be added to the whitelist
        Returns:
            bool: Returns true if the operation was completed successfully
        """
        if (self.is_registered(alias)):
            #   Don't add the alias to the list if it already exists
            log("[*] User is already registered for the chat room. Cancelling operation", "w")
            return False

        self.member_list.append(alias)
        return True

    def get_messages(self, num_messages: int=GET_ALL_MESSAGES, return_objects: bool=True) -> list:
        """Retrieve the ChatRoom's messages from storage. Also retrieves new messages from RMQ. 
        Users have the option of returning the objects as ChatMessage objects, or just the message content

        Args:
            num_messages (int, optional): Number of messages to retrieve from the message queue. Defaults to GET_ALL_MESSAGES
            return_objects (bool, optional): Flag indicating if the method should return ChatMessage 
            objects, or strings. Defaults to True (ChatMessage objects).

        Returns:
            list: List of messages associated with the ChatRoom object and the amount of strings retreived
        """
        log(f"[*] Requested retrieval of {GET_ALL_MESSAGES} from our queue of messages")
        self.__retrieve_messages()
        log(f"[*] Number of messages in internal queue {self.length}")
        if num_messages == GET_ALL_MESSAGES:
            if return_objects:
                return list(self), self.length
            else:
                serialized_list = [message.to_dict() for message in list(self)]
                return serialized_list, self.length
        else:
            messages = list()
            cur_num_messages = 0
            for message in list(self):
                if cur_num_messages < num_messages:
                    #   If return objects flag is raised, append ChatMessage object, otherwise append dict representation
                    message.append(message) if return_objects else message.append(message.message)
                    cur_num_messages += 1
                else:
                    return messages, cur_num_messages

    def send_message(self, message: str, mess_props: MessageProperties) -> bool:
        """Send message using RMQ. Also creates local message instance that is added to internal queue

        Args:
            message (str): Message to send to the chat application
            mess_props (MessageProperties): Properties of the message being sent
        Returns:
            bool: Return true if the message is successfully submitted to RMQ, false otherwise
        """
        try:
            self.rmq.channel.basic_publish(self.rmq.exchange_name, 
                                        routing_key=self.rmq.exchange_name,
                                        properties=pika.BasicProperties(headers=mess_props.__dict__),
                                        body=message, mandatory=True)
            log(f"[+] Succesfully published message to messaging server. Message: {message}")
            self.put(ChatMessage(message, mess_props))
            return True
        except pika.exceptions.UnroutableError:
            log(f"[-] Message was returned undeliverable.\n\tMessage: {message}\n\tTarget: {self.rmq.queue}")
            return False

    def find_message(self, message_text: str) -> ChatMessage:
        """Find message object in the deque using the text of the message as a key
        TODO: Transition to using unique oids

        Args:
            message_text (str): _description_
        Returns:
            ChatMessage: _description_
        """
        for chat_message in deque:
            if chat_message.message == message_text:
                return chat_message
        return None

    def get(self) -> ChatMessage:
        """Return the last message in the deque

        Returns:
            ChatMessage: Retrieved ChatMessage
        """
        try:
            return super()[-1]
        except: 
            log("[*] No messages in ChatRoom", 'd')

    def put(self, message: ChatMessage=None) -> None:
        """Puts message into the dequeue. Overrides default put method to place ChatMessages
        into the left end of the deque. We choose to read from the right

        Args:
            message (ChatMessage): _description_
        """
        log("[*] Put message: {message}")
        if message is not None:
            super().appendleft(message)
            self.__persist()

    def to_dict(self) -> dict:
        """Custom to_dict method for ChatRoom objects. The custom approach is designed
        to help make interactions with the MongoDB easier

        Returns:
            dict: Dictionary representation of the ChatRoom object
        """
        return {
            'room_name': f"{self.room_name}",
            'room_type': f"{self.room_type}",
            'create_time': f"{self.__create_time}",
            'modify_time': f"{self.__modify_time}",
            'member_list': self.member_list
        }

    def __metadata(self) -> dict:
        return {
            "room_name": self.room_name,
            "room_type": self.room_type
        }

    def __str__(self) -> str:
        return f"ChatRoom(Room Name: {self.room_name} Room Type: {self.room_type} Members: {self.member_list})"