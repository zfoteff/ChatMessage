""" """
__version__ = "1.0.0."
__author__ = "Zac Foteff"

from bin.constants import *
from bin.logger import Logger
from datetime import datetime

log = Logger("users")

class ChatUser():
    """Chat room user class object. Users must register using the application to send and recieve messages
    """

    def __init__(self, 
                alias: str,
                user_id=None,
                create_time: datetime=datetime.now(), 
                modify_time: datetime=datetime.now()) -> None:
        """Initialize a new User object. Mark the user as dirty by default, unless the user was restored 
        from the MongoDB collection

        Args:
            alias (str): Alias of the user
            user_id (_type_, optional): Unique identifier for the User object. Defaults to None.
            create_time (datetime, optional): Create time for the object. Defaults to datetime.now().
            modify_time (datetime, optional): Last time the object was modifieds. Defaults to datetime.now().
        """
        self.__alias = alias
        self.__user_id = user_id
        self.__create_time = create_time
        self.__modify_time = modify_time
        if self.__user_id is not None:
            self.__dirty = False
        else:
            self.__dirty = True

    @property
    def alias(self) -> str:
        return self.__alias

    @property
    def user_id(self) -> str:
        return self.__user_id

    def to_dict(self) -> dict:
        """Return a dictionary representation of the ChatUser object

        Returns:
            dict: Dictionary representation of object
        """
        return {
            "alias": self.alias,
            "create_time": self.__create_time,
            "modify_time": self.__modify_time
        }

    def __str__(self) -> str:
        return f"User (alias={self.alias}, id={self.user_id}"

