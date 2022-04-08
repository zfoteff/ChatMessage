"""UserList class object"""

__version__ = "1.0.0."
__author__ = "Zac Foteff"

from datetime import datetime
from pymongo import MongoClient
from bin.logger import Logger
from bin.constants import *
from src.chat_user import ChatUser

log = Logger("userList")


class UserList:
    """List of ChatUsers. Inherits from List class
    """

    def __init__(self, list_name: str = DB_DEFAULT_USER_LIST) -> None:
        """Initialize a new UserList object.
        NOTE: Depends on the ChatUser object as a dependency

        Args:
            list_name (str, optional): ID of the user list. Defaults to DB_DEFAULT_USER_LIST.
        """
        self.__list_name = list_name
        self.__user_list = list()
        self.__dirty = True
        self.__mongo_client = MongoClient(DB_HOST, DB_PORT)
        self.__mongo_db = self.__mongo_client.cpsc313
        self.__mongo_collection = self.__mongo_db.users
        self.__create_time = datetime.now()
        self.__modify_time = datetime.now()

        if self.__restore():
            log(f"[*] Successfully restored user list from MongoDB collection")
            self.__dirty = False
        else:
            log("[*] Cannot find user list in MongoDB. Creating new object . . .", 'w')

    @property
    def list_name(self) -> str:
        return self.__list_name

    @property
    def user_list(self) -> list:
        return self.__user_list

    @property
    def dirty(self) -> bool:
        return self.__dirty

    @property
    def _mongo_client(self):
        """Protected propety for testing"""
        return self.__mongo_client

    def __persist(self) -> None:
        """ First save a document that describes the user list (name of list, create and modify times)
        Second, for each user in the list create and save a document for that user
        """
        if self.__mongo_collection.find_one({'list_name': {'$exists': 'true'}}):
            list_update_filter = {'list_name': self.list_name}
            new_values = {"$set": self.to_dict()}
            self.__mongo_collection.update_one(list_update_filter, new_values, upsert=True)
            log("[+] Saved user list metadata to MongoDB")

        for user in self.user_list:
            user_update_filter = {'alias': user.alias}
            new_values = {"$set": user.to_dict()}
            self.__mongo_collection.update_one(user_update_filter, new_values, upsert=True)
        log("[+] Saved all users to user list collection")

    def __restore(self) -> bool:
        """ First get the document for the queue itself, then get all documents that are not the queue metadata
        """
        metadata = self.__mongo_collection.find_one({'list_name': {'$exists': 'true'}})
        if metadata is None:
            log("[*] No metadata found for ChatRoom object", 'e')
            return False
        self.__list_name = metadata['list_name']
        self.__create_time = metadata['create_time']
        self.__modify_time = metadata['modify_time']
        for user_dict in self.__mongo_collection.find({'alias': {'$exists': 'true'}}):
            self.__user_list.append(ChatUser(alias=user_dict['alias'], user_id=user_dict['_id']))
        log("[+] Restored all users to the user list")
        return True

    def register(self, new_alias: str) -> None:
        """Register new user to the user list. The method first checks if the new alias exists in the Database. If the 
        alias does not exist, a new user is created with that alias, and the method returns true. If the alias does 
        already exist, the method returns false and logs the reason to the log file 

        Args:
            new_alias (str): New alias of the user attempting to register
        Returns:
            bool: Returns true if the user is created in the database, false if the user already exists
        """
        if self.get(new_alias) is not None:
            log(f"[*] User {new_alias} already exists in the list of registered users. Cancelling operation . . .", 'e')
            return

        new_user = ChatUser(new_alias)
        self.__user_list.append(new_user)
        self.__modify_time = datetime.now()
        self.__persist()
        log(f"[+] {new_user} registered to user list {self.list_name}")

    def get(self, target_alias: str) -> ChatUser | None:
        """Find a user using their alias in the UserList. Should 
        return none if no entry is found with that alias

        Args:
            target_alias (str): Alias to query the database for
        Returns:
            ChatUser: Returns the chat user found in the user list. If nothing
            is found, None is returned
        """
        for user in self.user_list:
            if user.alias == target_alias:
                return user
        return None

    def get_all_users(self) -> list:
        """Returns a list of all user alias's in the user list

        Returns:
            list: List of users in the user list
        """
        return [user.alias for user in self.user_list]

    def to_dict(self) -> dict:
        return {
            "list_name": self.list_name,
            "create_time": f"{self.__create_time}",
            "modify_time": f"{self.__modify_time}"
        }

    def __str__(self) -> str:
        return f"UserList: {self.list_name} ({self.user_list})"
