"""Description"""

__version__ = "1.0.0"
__author__ = "Zac Foteff"

from src.message_props import MessageProperties
from bin.logger import Logger
from bin.constants import *

log = Logger("chatMessageHandler")


class ChatMessage:
    def __init__(self, message: str, mess_props: MessageProperties = None):
        """Instantiates a ChatMessage object. The object contains a message to be stored in the MongoDB to be 
        delivered to a user later. The object also contains all necessary properties and metadata of the message
        with a MessageProperties object
        NOTE: Requires the MessageProperties object as a dependency

        Args:
            message (str): The message the sending user would like to send to the application
            mess_props (MessageProperties, optional): Metadata object for message properties and information. Defaults to None.
        """
        if mess_props is None:
            #   If no message properties are supplied, autogenerate properties with placeholder values
            log("[-] No message properties included with submitted message. Auto populating ...", 'w')
            mess_props = MessageProperties(MESSAGE_SENT, 'Auto generated properties', "Unknown", "Unknown")
    
        self.__message = message
        self.__mess_props = mess_props
        self.__dirty = True

    @property
    def message(self) -> str:
        return self.__message

    @property
    def mess_props(self) -> MessageProperties:
        return self.__mess_props

    @property
    def dirty(self) -> bool:
        return self.__dirty

    @dirty.setter
    def dirty(self, new_dirty) -> None:
        self.__dirty = new_dirty

    def to_dict(self) -> dict:
        """Custom to_dict method for ChatMessage objects. The custom approach is designed
        to help make interactions with the MongoDB easier

        Returns:
            dict: Dictionary representation of the ChatMessage object
        """
        return {
            'message': f"{self.message}",
            'mess_props': self.mess_props.to_dict()
        }

    def __str__(self) -> str:
        return f"[+] Created new message\nMessage: {self.message}{self.mess_props}"
