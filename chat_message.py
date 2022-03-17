"""
"""

from bin.logger import Logger
from message_props import MessageProperties

logger = Logger("chatMessageHandler")

class ChatMessage:
    def __init__(self, message: str, mess_pros: MessageProperties, dirty: bool):
        self.message = message
        self.mess_props = mess_pros
        self.dirty = dirty

    @property
    def message(self) -> str:
        return self.message
    
    @property
    def mess_props(self) -> MessageProperties:
        return self.mess_props
    
    @property
    def dirty(self) -> bool:
        return self.dirty
    
    def __str__(self) -> str:
        return (f"[+] Created new message. Message: {self.message}{self.mess_props}")