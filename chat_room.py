"""
Class for interactions with MongoDB and RabbitMQ to create a Chat Room instance

@author Zac Foteff
@version 1.0.0.
"""

from collections import deque
from bin.logger import Logger
from message_props import MessageProperties
from chat_message import ChatMessage
from rmq import RMQMessageInteractions
from db_helper import ChatRoomDBHelper
import time

ROOM_TYPE_PUBLIC = 100
ROOM_TYPE_PRIVATE = 200

logger = Logger("chatRoom")


class ChatRoom(deque):
    def __init__(self, room_name: str,
                 owner_alias: str,
                 member_list=None,
                 room_type: int = ROOM_TYPE_PUBLIC,
                 create_new: bool = False,
                 create_time: float = time.time(),
                 modify_time: float = time.time()):
        """ChatRoom class object constructor

        Args:
            room_name (str): Room name. Default queue_name for consuming is using message queues
            member_list (list): _description_
            owner_alias (str): _description_
            room_type (int): _description_
            create_new (bool): _description_
            create_time (float): _description_
            modify_time (float): _description_
        """
        super().__init__()

        if member_list is None:
            member_list = []

        self.room_name = room_name
        self.member_list = member_list
        self.owner_alias = owner_alias
        self.room_type = room_type
        self.create_new = create_new
        self.create_time = create_time
        self.modify_time = modify_time

    @property
    def room_name(self):
        """
        Channel and exchange name

        Returns:
            _type_: _description_
        """
        return self.room_name

    @property
    def owner(self):
        return self.owner_alias

    @property
    def room_type(self):
        return self.room_type

    @property
    def members(self):
        return self.member_list

    def __retrieve_messages(self):
        """
        Restore messages from

        Returns:

        """
        pass

    def add_group_member(self):
        pass

    def get_messages(self, num_message: int, return_objects: bool):
        pass

    def send_message(self, message: str, mess_props: MessageProperties):
        pass

    def find_message(self, message_text: str):
        pass

    def get(self):
        pass

    def put(self, message: ChatMessage):
        pass
