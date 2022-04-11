"""
Class for interactions with MongoDB and RabbitMQ to create a Chat Room instance
"""

__author__ = "Zac Foteff"
__version__ = "2.0.0."

from datetime import datetime
from pymongo import MongoClient, ReturnDocument
from collections import deque
from src.chat_user import ChatUser
from src.user_list import UserList
from src.message_props import MessageProperties
from src.chat_message import ChatMessage
from bin.constants import *
from bin.logger import Logger

log = Logger("chatRoom")

class ChatRoom(deque):
    """ChatRoom class object. Inherits from dequeue to create an internal cache of ChatMessage objects"""
    def __init__(
            self,
            room_name: str,
            room_type: int = CHAT_ROOM_TYPE_PUBLIC,
            owner_alias: str = "",
            create_time: datetime = datetime.now(),
            modify_time: datetime = datetime.now()):
        """Instantiate a ChatRoom class object. All properties are created in the constructor, or
        restored from an existing entry in storage

        Args:
            room_name (str): Room name. Default queue_name for consuming is using message queues
            owner_alias (str): Alias of the room creator
            room_type (int, optional): Type of room. Defaults to CHAT_ROOM_TYPE_PUBLIC
            create_time (datetime, optional): Time that the room was created
            modify_time (datetime, optional): Last time that the room was modified
        """
        super(ChatRoom, self).__init__()
        self.__room_name = room_name
        self.__owner_alias = owner_alias
        self.__member_list = UserList(self.__room_name)
        self.__room_type = room_type
        self.__dirty = True
        self.__removed = False
        self.__create_time = create_time
        self.__modify_time = modify_time

        #   Initialize MongoDB resources
        # PROD ONLY: self.__mongo_client = MongoClient(PROD_DB_HOST, PROD_DB_PORT)
        self.__mongo_client = MongoClient(TEST_DB_HOST)
        self.__mongo_db = self.__mongo_client.cpsc313
        self.__mongo_collection = self.__mongo_db.get_collection(room_name)
        self.__mongo_seq_collection = self.__mongo_db.get_collection('sequence')

        if self.__mongo_collection is None:
            #   Initialize the chat queue collection in the DB if it does not already exist
            log(f"[-] No collection for chat room {self.__room_name} in the database. Creating . . .")
            self.__mongo_collection = self.__mongo_db.create_collection(room_name)

        if self.__mongo_seq_collection is None:
            #   Initialize the sequence number collection in the DB if it does not already exist
            log("[-] No sequence collection in the database. Creating . . .")
            self.__mongo_seq_collection = self.__mongo_db.create_collection('sequence')

        if self.__restore():
            #   Element is restored from storage, so indicate there are no changes to be saved
            self.__dirty = False

    @property
    def room_name(self) -> str:
        return self.__room_name

    @property
    def member_list(self) -> UserList:
        return self.__member_list

    @property
    def dirty(self) -> bool:
        return self.__dirty

    @dirty.setter
    def dirty(self, new_dirty) -> None:
        self.__dirty = new_dirty

    @property
    def removed(self) -> bool:
        return self.__removed

    @removed.setter
    def removed(self, new_removed) -> None:
        self.__removed = new_removed

    @property
    def room_type(self) -> int:
        return self.__room_type

    @property
    def owner_alias(self) -> str:
        return self.__owner_alias

    @owner_alias.setter
    def owner_alias(self, new_owner_alias) -> None:
        self.__owner_alias = new_owner_alias

    @property
    def member_list(self) -> UserList:
        return self.__member_list

    @property
    def length(self) -> int:
        return len(self)

    def __persist(self) -> None:
        """Persist object data in MongoDB. First, save the user list if it isn't already there
        or there are changes that need to be persisted. Next, for each message in the list create
        and save a document for that user
        """
        if self.__mongo_collection.find_one({'room_name': {'$exists': 'false'}}) is None:
            room_update_filter = {'room_name': self.room_name}
            new_values = {"$set": self.to_dict()}
            self.__mongo_collection.update_one(room_update_filter, new_values, upsert=True)

        for message in list(self):
            message_update_filter = {'message': message.message}
            new_values = {"$set": message.to_dict()}
            self.__mongo_collection.update_one(message_update_filter, new_values, upsert=True)

    def __restore(self) -> bool:
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
        metadata = self.__mongo_collection.find_one({'room_name': {'$exists': 'true'}})
        if metadata is None:
            log("[*] No metadata found for ChatRoom object. Creating new collection . . .", 'w')
            self.__persist()
            return False

        self.__room_name = metadata['room_name']
        self.__room_type = metadata['room_type']
        self.__create_time = metadata['create_time']
        self.__modify_time = metadata['modify_time']
        for mess_data in self.__mongo_collection.find({'message': {'$exists': 'true'}}):
            new_mess_props = MessageProperties(
                mess_data['mess_props']['mess_type'],
                mess_data['mess_props']['room_name'],
                mess_data['mess_props']['to_user'],
                mess_data['mess_props']['from_user'],
                mess_data['mess_props']['sequence_num'],
                mess_data['mess_props']['sent_time'],
                mess_data['mess_props']['rec_time'])
            new_message = ChatMessage(mess_data['message'], new_mess_props)
            self.put(new_message)
        log(f"[+] Restored ChatRoom object {self.to_dict()}")
        return True

    def __get_next_sequence_num(self) -> int:
        """Queries the sequence number collection from MongoDB and selects the next 
        sequence number to assign to the message. Returns a sequence number of -1 if there is an err

        Returns:
            int: Next sequence number to assign to new messages. Returns -1 on 
        """
        try:
            sequence_num = self.__mongo_seq_collection.find_one_and_update(
                {'_id': 'userid'},
                {'$inc': {self.room_name: 1}},
                projection={self.room_name: True, '_id': False},
                upsert=True,
                return_document=ReturnDocument.AFTER)
        except: 
            sequence_num = -1

        return sequence_num

    def add_group_member(self, alias: str) -> bool:
        """Register new user to the room's list of Users. Takes an alias and returns True if
        the user isn't registered to the room, and they were successfully added. Will return False
        if the user was already registered in the room, or an error prevents them from being added

        Args:
            alias (str): Alias of the user to be added to the whitelist
        Returns:
            bool: Returns true if the operation was completed successfully
        """
        if self.member_list.register(alias):
            self.__modify_time = datetime.now()
            self.__persist()
            return True
        return False

    def get_group_member(self, alias: str) -> ChatUser | None:
        """Get a user that exists in the ChatRoom. Returns the chat user if the alias matches, otherwise the method
        returns None

        Args:
            alias (str): Alias to search the member list for 
        Returns:
            ChatUser | None: Returns ChatUser with matching alias, or None if the alias can't be found
        """
        return self.member_list.get(alias)

    def get_messages(self, alias: str, num_messages: int=GET_ALL_MESSAGES, return_objects: bool=False) -> list:
        """Retrieve the ChatRoom's messages from storage. Also retrieves new messages from Mongo. 
        Users have the option of returning the objects as ChatMessage objects, or just the message 
        content. The method will also filter the messages to ensure that no blocked users' messages
        are included in the list of returned messages

        Args:
            alias (str): Alias of the user requesting the messages
            num_messages (int, optional): Number of messages to retrieve from the message queue. 
            Defaults to GET_ALL_MESSAGES
            return_objects (bool, optional): Flag indicating if the method should return ChatMessage 
            objects if True, or strings if False. Defaults to False.
        Returns:
            list: List of messages associated with the ChatRoom object and the amount of strings 
            retrieved
        """

        requesting_user = self.get_group_member(alias)
        message_container = list()
        log(f"[*] Requested {GET_ALL_MESSAGES} messages. Requesting user: {requesting_user}. Number of messages in internal queue: {self.length}")
        
        if num_messages == GET_ALL_MESSAGES or num_messages > self.length:
            for message in list(self):
                if message.mess_props.from_user not in requesting_user.blocked_users:
                    #   Message should only continue to be checked if the sender is not in the recievers blocker user list
                    if message.mess_props.rec_time == None:
                        #   If the message has not been recieved yet, acknowledge the message in the mess_type, rec_time, and the dirty flag
                        message.mess_props.rec_time = datetime.now()
                        message.mess_props.mess_type = MESSAGE_RECEIVED
                        message.dirty = True

                    message_container.append(message) if return_objects else message_container.append(message.message)

        else:
            for message_iterator in range(0, num_messages):
                message = list(self)[message_iterator]
                if message.mess_props.from_user not in requesting_user.blocked_users:
                    #   Message should only continue to be checked if the sender is not in the recievers blocker user list
                    if message.mess_props.rec_time == None:
                        #   If the message has not been recieved yet, acknowledge the message in the mess_type, rec_time, and the dirty flag
                        message.mess_props.rec_time = datetime.now()
                        message.mess_props.mess_type = MESSAGE_RECEIVED
                        message.dirty = True

                    message_container.append(message) if return_objects else message_container.append(message.message)

        return message_container

    def send_message(self, message: str, room_name: str, from_alias: str, to_alias: str) -> bool:
        """Insert message into the message list for the room, and create a mongodb document 
        for the message. The MessageProperties should be constructed and attached to the message 
        before it is place in the deque + database. The ChatRoom first is checked if the from and 
        to alias's are in the registered user list (if the )

        Args:
            message (str): Message to send to the chat application
            room_name (str): Room to send the message to
            from_alias (str): Alias of the user who sent the message
            to_alias (str): Alias of the user the message is intended for
        Returns:
            bool: Return true if the message is successfully sent, false otherwise
        """
        if self.room_type == CHAT_ROOM_TYPE_PRIVATE and from_alias in self.member_list.get_all_users() and to_alias in self.member_list.get_all_users():
            mess_props = MessageProperties(
                mess_type=MESSAGE_SENT,
                room_name=room_name,
                from_user=from_alias,
                to_user=to_alias,
                sequence_num=self.__get_next_sequence_num())
            new_message = ChatMessage(message=message, mess_props=mess_props)
            self.put(new_message)
            return True

        elif self.room_type == CHAT_ROOM_TYPE_PUBLIC

    def find_message(self, message_text: str) -> ChatMessage | None:
        """Find message object in the deque using the text of the message as a key
        
        TODO: Transition to using unique oids

        Args:
            message_text (str): _description_
        Returns:
            ChatMessage: _description_
        """
        for chat_message in list(self):
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

    def put(self, message: ChatMessage) -> None:
        """Puts message into the dequeue. Overrides default put method to place ChatMessages
        into the left end of the deque. We choose to read from the right. Method also saves the 
        new messages into the db

        Args:
            message (ChatMessage): ChatMessage to send to place in the deque and to persist in 
            the db
        """
        log(f"[*] Put message: {message}", 'd')
        super().appendleft(message)
        self.__modify_time = datetime.now()
        self.__persist()

    def metadata(self) -> dict:
        """Custom method to return metadata. This method is used by ther room_list to store 
        metadata in its internal room list. Metadata is composed of the
            * Room name
            * Room type
            * Owner alias

        Returns:
            dict: Metadata for this ChatRoom object
        """
        return {
            'room_name': self.__room_name,
            'room_type': self.__room_type,
            'owner_alias': self.__owner_alias
        }

    def to_dict(self) -> dict:
        """Custom to_dict method for ChatRoom objects. The custom approach is designed
        to help make interactions with the MongoDB easier

        Returns:
            dict: Dictionary representation of the ChatRoom object
        """
        return {
            'room_name': self.__room_name,
            'owner_alias': self.__owner_alias,
            'room_type': self.__room_type,
            'member_list': self.__member_list.to_dict(),
            'create_time': f"{self.__create_time}",
            'modify_time': f"{self.__modify_time}"
        }

    def __str__(self) -> str:
        return f"ChatRoom(Room Name: {self.room_name} Room Type: {self.room_type} Members: {self.member_list})"
