"""
Class for interactions with MongoDB and RabbitMQ
"""

from bin.logger import Logger
from collections import deque

logger = Logger("chatRoom")

class ChatRoom(deque):
    def __init__(self, room_name: str, group_room: bool, owner_alias: str, members: list, dirty: bool, create_time: str, modify_time: str):
        self.room_name = room_name
        self.group_room = group_room
        self.owner_alias = owner_alias
        self.members = members
        self.is_dirty = dirty
        self.create_time = create_time
        self.modify_time = modify_time
        
    @property
    def room_name(self):
        return self.room_name