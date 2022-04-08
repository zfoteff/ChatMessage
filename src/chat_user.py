__version__ = "1.0.0."
__author__ = "Zac Foteff"

from bin.logger import Logger
from datetime import datetime

log = Logger("users")


class ChatUser:
    """Chat room user class object. Users must register using the application to send and receive messages
    """

    def __init__(self,
                 alias: str,
                 user_id=None,
                 blocked_users=None,
                 create_time: datetime = datetime.now(),
                 modify_time: datetime = datetime.now()) -> None:
        """Initialize a new User object. Mark the user as dirty by default, unless the user was restored from the
        MongoDB collection

        Args:
            alias (str): Alias of the user
            user_id (_type_, optional): Unique identifier for the User object. Defaults to None.
            create_time (datetime, optional): Create time for the object. Defaults to datetime.now().
            modify_time (datetime, optional): Last time the object was modified. Defaults to datetime.now().
        """
        if blocked_users is None:
            self.__blocked_users = list()
        self.__alias = alias
        self.__user_id = user_id
        self.__blocked_users = blocked_users
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

    @property
    def blocked_users(self) -> list:
        return self.__blocked_users

    @property
    def dirty(self) -> bool:
        return self.__dirty

    @dirty.setter
    def dirty(self, new_dirty) -> None:
        self.__dirty = new_dirty

    def block_user(self, block_alias: str) -> None:
        """Block a users messages from being received by this user. Adds the alias to the user's internal list of
        blocked users

        Args:
            block_alias (str): User alias to block
        """
        if self.is_blocked(block_alias):
            log(f"[*] User {block_alias} is already blocked")
            return

        self.__blocked_users.append(block_alias)
        log(f"[+] Blocked user {block_alias}")

    def is_blocked(self, alias: str) -> bool:
        """Checks if a user is in this user's list of blocked users

        Args:
            alias (str): User alias to look for in the blocked list
        Returns:
            bool: true if alias is in the list, false otherwise
        """
        return alias in self.__alias

    def to_dict(self) -> dict:
        """Return a dictionary representation of the ChatUser object

        Returns:
            dict: Dictionary representation of object
        """
        return {
            "alias": self.__alias,
            "blocked_users": self.__blocked_users,
            "create_time": self.__create_time,
            "modify_time": self.__modify_time
        }

    def __str__(self) -> str:
        return f"User (alias={self.alias}, id={self.user_id})"
