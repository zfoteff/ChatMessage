from datetime import datetime
from pymongo import MongoClient
from bin.logger import Logger
from bin.constants import *
from src.users import ChatUser

log = Logger("userList")

class UserList():
    """List of ChatUsers. Inherits from List class
    """
    def __init__(self, list_name: str=DB_DEFAULT_USER_LIST) -> None:
        """Initialize a new UserList object

        Args:
            list_name (str, optional): ID of the user list. Defaults to DB_DEFAULT_USER_LIST.
        """
        self.__user_list = list()
        self.__list_name = list_name
        self.__mongo_client = MongoClient(DB_HOST, DB_PORT)
        self.__mongo_db = self.__mongo_client.cpsc313
        self.__mongo_collection = self.__mongo_db.users

        if self.__restore():
            log(f"[*] Successfully restored userlist from MongoDB collection")
            self.__dirty = False
        else:
            log("[*] Cannot find userlist in MongoDB. Creating new object . . .", 'w')
            self.__dirty = True

    @property
    def list_name(self) -> str:
        return self.__list_name

    @property
    def user_list(self) -> list:
        return self.__user_list

    @property
    def _mongo_client(self):
        return self.__mongo_client

    def __persist(self) -> bool:
        """ First save a document that describes the user list (name of list, create and modify times)
        Second, for each user in the list create and save a document for that user
        """
        if self.__mongo_collection.find_one({'list_name': {'$exists': 'false'}}) is None:
            self.__mongo_collection._insert_one({
                'list_name': self.list_name,
                'create_time': self.__create_time,
                'modify_time': self.__modify_time
            })

        for user in self.user_list:
            if user.dirty:
                serialized = user.to_dict()
                self.__mongo_collection.insert_one(serialized)
                user.dirty = False

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
        self.__user_list = list()
        for user_dict in self.__mongo_collection.find({'alias': {'$exists': 'true'}}):
            self.__user_list.append(ChatUser(alias=user_dict['alias'], user_id=user_dict['_id']))
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
        self.__dirty = True
        self.__persist()
        log(f"[+] User {new_user} registered to user list {self.list_name}")

    def get(self, target_alias: str) -> ChatUser:
        """Find a user using their alias in the UserList. Should 
        return none if no entry is found with that alias

        Args:
            target_alias (str): Alias to query the database for
        Returns:
            ChatUser: Returns the chat user found in the userlist. If nothing 
            is found, None is returned
        """
        for user in self.user_list:
            if user.alias == target_alias:
                return user
        return None

    def get_all_users(self) -> list:
        return [user.alias for user in self.user_list]

    def to_dict(self) -> dict:
        return {
            "list_name": self.list_name,
            "members": self.user_list
        }

    def __str__(self) -> str:
        return f"UserList: {self.list_name} ({self.user_list})"