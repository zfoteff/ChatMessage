from users import ChatUser
from pymongo import MongoClient
from bin.logger import Logger
from bin.constants import *

log = Logger("userList")

class UserList():
    """List of ChatUsers. Inherits from List class
    """
    def __init__(self, list_name: str=DB_DEFAULT_USER_LIST) -> None:
        self.__user_list = list()
        self.__mongo_client = MongoClient(DB_HOST, DB_PORT)
        self.__mongo_db = self.__mongo_client.detest
        self.__mongo_collection = self.__mongo_db.DB_USER_LIST_COLLECTION

        if self.__restore():
            log(f"[*] Successfully restored")
            self.__dirty = False
        else:
            log("[*] Cannot find userlist in MongoDB. Creating new object . . .", 'w')
            self.__dirty = True

    @property
    def user_list(self) -> list:
        return self.__user_list

    def __persist(self) -> bool:
        """ First save a document that describes the user list (name of list, create and modify times)
        Second, for each user in the list create and save a document for that user
        """
        pass

    def __restore(self) -> bool:
        """ First get the document for the queue itself, then get all documents that are not the queue metadata
        """
        pass

    def register(self, new_alias: str) -> bool:
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
            return False
        new_user = ChatUser(new_alias)
        self.__user_list.append(new_user)
        return True


    def get(self, target_alias: str) -> ChatUser:
        """Find a user using their alias in the MongoDB collection

        Args:
            target_alias (str): Alias to query the database for
        Returns:
            ChatUser: Returns the chat user found in the database. If nothing is found, None is returned
        """
        
        return None

    def get_all_users(self) -> list:
        return [user.alias for user in self.user_list]