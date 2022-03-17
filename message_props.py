"""
Message properties object class file

@author Zac Foteff
@version 1.0.0.
"""

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
                rec_time: datetime=datetime.now()):
        """Instantiate a new MessageProperties class object. The object encapsulates
        all the properties of messages that are sent using the chat application API

        Args:
            sequence_number (int): Location of the message in the sequence of messages that exist in the room
            id (int): Unique identifier of the message
            mess_type (str): Type of the message. Defaults to recieved
            room_name (str): Name of the room that the message is sent in
            to_user (str): Alias of the user the message should be sent to
            from_user (str): Alias of the user who sent the message
            sent_time (datetime): Time the message was recieved by the system
            rec_time (datetime): Time the message was recieved by the system
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

    @property
    def message_type(self) -> str:
        return self.__mess_type

    @property
    def to_user(self) -> str:
        return self.__to_user

    @property
    def from_user(self) -> str:
        return self.__from_user

    @property 
    def sent_time(self) -> str:
        return self.__sent_time

    @property
    def rec_time(self) -> str:
        return self.__rec_time

    def to_dict(self) -> dict:
        """Custom to_dict method for message property objects. The custom approach is designed
        to help make interactions with the MongoDB easier

        Returns:
            dict: Dictionary representation of the MessageProperty object
        """
        return {
            "id": f"{self.id}",
            "sequence_number": f"{self.sequence_number}",
            "room": f"{self.room_name}",
            "sender": f"{self.from_user}",
            "sent_time": f"{self.sent_time}",
            "reciever": f"{self.to_user}",
            "recieved_time": f"{self.rec_time}",
        }

    def __str__(self) -> str:
        return (f"Message properties"
               +f"\n\tID: {self.id} Sequence number: {self.sequence_number}\n\t"
               +f"\n\tRoom: {self.room_name} Sender: {self.from_user} | {self.sent_time} Receiever: {self.to_user} | {self.rec_time}")