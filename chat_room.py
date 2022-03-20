"""
Class for interactions with MongoDB and RabbitMQ to create a Chat Room instance
"""

__author__ = "Zac Foteff"
__version__ = "1.0.0."

import time
from pymongo import MongoClient
from collections import deque
from bin.logger import Logger
from message_props import MessageProperties
from chat_message import ChatMessage
from rmq import RMQMessageInteractions
from db_helper import ChatRoomDBHelper
from bin.constants import *

log = Logger("chatRoom")

class ChatRoom(deque):
    def __init__(self, room_name: str,
                 owner_alias: str,
                 member_list: list=None,
                 room_type: int=CHAT_ROOM_TYPE_PUBLIC,
                 dirty: bool=False,
                 create_time: float=time.time(),
                 modify_time: float=time.time()):
        """Intantiate a ChatRoom class object. Requires a room name and an owner alias by default.
        All other properties are created in the constructor, or restored from an existing entry in 
        storage

        Args:
            room_name (str): Room name. Default queue_name for consuming is using message queues
            member_list (list): List of all registered members to the chatroom
            owner_alias (str): Alias of the room creator
            room_type (int, optional): Type of room. Defaults to public
            create_new (bool, optional): Flag indicating if the chat room exists in the database 
            create_time (float, optional): Time that the room was created
            modify_time (float, optional): Last time that the room was modified
        """
        super(ChatRoom, self).__init__()

        if member_list is None:
            member_list = []

        self.__room_name = room_name
        self.__member_list = member_list
        self.__owner_alias = owner_alias
        self.__room_type = room_type
        self.__dirty = dirty
        self.__create_time = create_time
        self.__modify_time = modify_time
        self.__mongo_collection = ChatRoomDBHelper()

    @property
    def room_name(self):
        return self.__room_name

    @property
    def owner(self) -> str:
        return self.__owner_alias

    @property
    def room_type(self) -> int:
        return self.__room_type

    @property
    def members(self) -> list:
        return self.__member_list

    @property
    def dirty(self) -> bool:
        return self.__dirty

    def __retrieve_messages(self):
        """
        Restore messages specific to the ChatRoom from storage

        Returns:
            list(ChatMessage): List of chat messages retrieved from storage
        """
        pass

    def __persist(self):
        pass

    def __restore(self):
        pass

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

        self.members.append(alias)
        return True

    def get_messages(self, num_messages: int, return_objects: bool=True) -> list:
        """Retrieve the ChatRoom's messages from storage. Users have the option of returning the objects
        as ChatMessage objects, or as JSON representations of ChatMessage objects

        Args:
            num_messages (int): Number of messages to retrieve from the message queue
            return_objects (bool, optional): Flag indicating if the method should return ChatMessage 
            objects, or JSON responses. Defaults to True (ChatMessage objects).

        Returns:
            list: List of messages associated with the ChatRoom object
        """
        pass

    def send_message(self, message: str, mess_props: MessageProperties) -> bool:
        """Send message

        Args:
            message (str): _description_
            mess_props (MessageProperties): _description_
        Returns:
            bool: _description_
        """
        pass

    def find_message(self, message_text: str) -> ChatMessage:
        """_summary_

        Args:
            message_text (str): _description_
        Returns:
            ChatMessage: _description_
        """
        pass

    def get(self) -> ChatMessage:
        """_summary_

        Returns:
            ChatMessage: _description_
        """
        pass

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
            'owner': f"{self.owner}",
            'create_time': f"{self.__create_time}",
            'modify_time': f"{self.__modify_time}",
            'create_new': self.create_new,
            'members': self.members
        }

    def __str__(self) -> str:
        return f"ChatRoom(Room Name: {self.room_name} Room Type: {self.room_type} Owner: {self.owner})"