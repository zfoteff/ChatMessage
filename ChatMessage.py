"""
"""

from bin.logger import Logger
from MessageProperties import MessageProperties

logger = Logger("chatMessageHandler")

class ChatMessage:
    def __init__(self, message: str, mess_pros: MessageProperties, dirty: bool):
        self.message = message
        self.mess_props = mess_pros
        self.dirty = dirty
        
    @property
    def message(self):
        return self.message
    
    @property
    def mess_props(self):
        return self.mess_props
    
    @property
    def dirty(self):
        return self.dirty
    
    def __str__(self):
        return (f"[+] Created new message. Message: {self.message}{self.mess_props}")