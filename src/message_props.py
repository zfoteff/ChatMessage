"""
Message properties object class file

@author Zac Foteff
@version 1.0.0.
"""
__version__ = "1.0.0"
__author__ = "Zac Foteff"

from datetime import datetime
from bin.logger import Logger

logger = Logger("messageProperties")


class MessageProperties:
    """
    MessageProperties class object
    """

    def __init__(self,
                 mess_type: int,
                 room_name: str,
                 to_user: str,
                 from_user: str,
                 sequence_num: int = -1,
                 sent_time: datetime = datetime.now(),
                 rec_time: datetime = None):
        """Instantiate a new MessageProperties class object. The object encapsulates
        all the properties of messages that are sent using the chat application API

        Args:
            mess_type (str): Type of the message. Defaults to recieved
            room_name (str): Name of the room that the message is sent in
            to_user (str): Alias of the user the message should be sent to
            from_user (str): Alias of the user who sent the message
            sequence_num (int, optional): Location of the message in the sequence of messages that exist in the
            room. Defaults to -1
            sent_time (datetime, optional): Time the message was received by the system. Defaults to the current time
            rec_time (datetime, optional): Time the message was received by the system. Defaults to None
        """
        self.__mess_type = mess_type
        self.__room_name = room_name
        self.__from_user = from_user
        self.__to_user = to_user
        self.__sequence_num = sequence_num
        self.__sent_time = sent_time
        self.__rec_time = rec_time

    @property
    def room_name(self) -> str:
        return self.__room_name

    @property
    def mess_type(self) -> int:
        return self.__mess_type

    @property
    def from_user(self) -> str:
        return self.__from_user

    @property
    def to_user(self) -> str:
        return self.__to_user

    @property
    def sequence_num(self) -> int:
        return self.__sequence_num

    @property
    def sent_time(self) -> datetime:
        return self.__sent_time

    @property
    def rec_time(self) -> datetime:
        return self.__rec_time

    def to_dict(self) -> dict:
        """Custom to_dict method for message property objects. The custom approach is designed
        to help make interactions with the MongoDB easier

        Returns:
            dict: Dictionary representation of the MessageProperty object
        """
        return {
            "mess_type": self.mess_type,
            "sequence_num": self.sequence_num,
            "room_name": f"{self.room_name}",
            "from_user": f"{self.from_user}",
            "sent_time": f"{self.sent_time}",
            "to_user": f"{self.to_user}",
            "rec_time": f"{self.rec_time}",
        }

    def __str__(self) -> str:
        return (f"\nMessage properties"
                + f"\n\tRoom: {self.room_name} Type: {self.mess_type} Sequence Number: {self.sequence_num}"
                + f"\n\tSender: {self.from_user} | {self.sent_time}\n\tReceiever: {self.to_user} | {self.rec_time}")
