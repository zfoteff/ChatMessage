"""
Message properties object class file

@author Zac Foteff
@version 1.0.0.
"""
__version__ = "1.0.0"
__author__ = "Zac Foteff"

from datetime import datetime
from bin.logger import Logger

MESSAGE_SENT = 0
MESSAGE_RECIEVED = 1

logger = Logger("messageProperties")

class MessageProperties:
    """
    MessageProperties class object
    """
    def __init__(self, 
                sequence_number: int, 
                id: int, 
                mess_type: str, 
                room_name: str, 
                to_user: str, 
                from_user: str,
                sent_time: datetime=datetime.now(),
                rec_time: datetime=None):
        """Instantiate a new MessageProperties class object. The object encapsulates
        all the properties of messages that are sent using the chat application API

        Args:
            sequence_number (int): Location of the message in the sequence of messages that exist in the room
            id (int): Unique identifier of the message
            mess_type (str): Type of the message. Defaults to recieved
            room_name (str): Name of the room that the message is sent in
            to_user (str): Alias of the user the message should be sent to
            from_user (str): Alias of the user who sent the message
            sent_time (datetime, optional): Time the message was recieved by the system. Defaults to the current time
            rec_time (datetime, optional): Time the message was recieved by the system. Defaults to None
        """
        self.__sequence_number = sequence_number
        self.__id = id
        self.__mess_type = mess_type
        self.__room_name = room_name
        self.__from_user = from_user
        self.__to_user = to_user
        self.__sent_time = sent_time
        self.__rec_time = rec_time
    
    @property
    def id(self) -> int:
        return self.__id
    
    @property
    def sequence_number(self) -> int:
        return self.__sequence_number
    
    @property
    def room_name(self) -> str:
        return self.__room_name

    def to_dict(self) -> dict:
        """Custom to_dict method for message property objects. The custom approach is designed
        to help make interactions with the MongoDB easier

        Returns:
            dict: Dictionary representation of the MessageProperty object
        """
        return {
            "id": self.id,
            "sequence_number": self.sequence_number,
            "room": f"{self.room_name}",
            "sender": f"{self.from_user}",
            "sent_time": f"{self.sent_time}",
            "reciever": f"{self.to_user}",
            "recieved_time": f"{self.rec_time}",
        }

    def __str__(self) -> str:
        return (f"\nMessage properties"
               +f"\n\tID: {self.id} Sequence number: {self.sequence_number}"
               +f"\n\tRoom: {self.room_name}"
               +f"\n\tSender: {self.from_user} | {self.sent_time}\n\tReceiever: {self.to_user} | {self.rec_time}")