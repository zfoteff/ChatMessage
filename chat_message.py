"""Description"""

__version__ = "1.0.0"
__author__ = "Zac Foteff"

from bin.logger import Logger
from message_props import MessageProperties

log = Logger("chatMessageHandler")

class ChatMessage:
    def __init__(self, message: str, mess_props: MessageProperties=None, dirty: bool=False):
        """Instantiates a ChatMessage object. The object contains a message to be stored in the MongoDB to be 
        delievered to a user later. The object also contains all necessary properties and metadata of the message
        with a MessageProperties object
        NOTE: Requires the MessageProperties object as a dependancy

        Args:
            message (str): The message the sending user would like to send to the application
            mess_props (MessageProperties, optional): Metadata object for message properties and information. Defaults to None.
            dirty (bool, optional): Indicates if the message has be altered and has changes that need to be recorded. Defaults to False.
        """
        if mess_props == None:
            #   If no message properties are supplied, autogenerate properties with placeholder values
            log("[-] No message properties included with submitted message. Auto populating ...", 'w')
            mess_props = MessageProperties(-1, -1, 'Auto generated properties', "bin", "Unknown", "Unknown")

        self.__message = message
        self.__mess_props = mess_props
        self.__dirty = dirty

    @property
    def message(self) -> str:
        return self.__message
    
    @property
    def mess_props(self) -> MessageProperties:
        return self.__mess_props
    
    @property
    def dirty(self) -> bool:
        return self.__dirty

    def to_dict(self) -> dict:
        """Custom to_dict method for ChatMessage objects. The custom approach is designed
        to help make interactions with the MongoDB easier

        Returns:
            dict: Dictionary representation of the ChatMessage object
        """
        return {
            'message': f"{self.message}",
            'dirty': self.dirty,
            'message_properties': self.mess_props.to_dict()
        }
    
    def __str__(self) -> str:
        return f"[+] Created new message\nMessage: {self.message}{self.mess_props}"