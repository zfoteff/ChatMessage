""" 
Room list dequeue implementation for managing declared channels on the 
messaging service
"""

__author__ = "Zac Foteff"
__version__ = "1.0.0."

from pymongo import MongoClient
from datetime import datetime
from bin.constants import *
from bin.logger import Logger
from src.chat_room import ChatRoom

log = Logger("./roomList")


class RoomList:
    """
    RoomList object class that stores all declared ChatRoom instances 
    """

    def __init__(self, list_name: str = DB_DEFAULT_ROOM_LIST) -> None:
        """
        Stores rooms in a list of dict of with the room name acting as 
        the key and the ChatRoom instance and a dirty flag as values. Should ensure 
        that if no room list is passed to the constructor, then the application 
        will try to restore a room list, or create a new list if no room list 
        is already stored in the database
        NOTE: Depends on the ChatRoom class object as a dependancy
        """
        self.__list_name = list_name
        self.__room_list = []
        self.__dirty = True
        self.__create_time = datetime.now()
        self.__modify_time = datetime.now()

        #   Initialize MongoDB resources
        # PROD ONLY: self.__mongo_client = MongoClient(PROD_DB_HOST, PROD_DB_PORT)
        self.__mongo_client = MongoClient(TEST_DB_HOST)
        self.__mongo_db = self.__mongo_client.cpsc313
        self.__mongo_collection = self.__mongo_db.get_collection(list_name)
        if self.__mongo_collection is None:
            #   Initialize the chat queue collection in the DB if it does not already exist
            self.__mongo_collection = self.__mongo_db.create_collection(list_name)

        if self.__restore():
            self.__dirty = False

    @property
    def list_name(self) -> str:
        return self.__list_name

    @property
    def room_list(self) -> list:
        return self.__room_list

    @property
    def dirty(self) -> bool:
        return self.__dirty

    @property
    def length(self) -> int:
        return len(self.__room_list)

    def __persist(self) -> None:
        """Persist a RoomList instance in  MongoDB. Create document using the ChatRoom instance room name
        as a key, then restore the ChatRoom instances that are declared for this instance of the application. Uses
        the update_one collection to minimize the amount of objects that are stored in the DB. Elements are selected
        using their unique room id.
        NOTE: the updaate_one method is used with the upsert flag raised to tell the system to create a new object if
        the object does not already exist in the DB
        """
        if self.__mongo_collection.find_one({'list_name': {'$exists': 'true'}}):
            filter = {'list_name': self.list_name}
            new_values = {"$set": self.to_dict()}
            self.__mongo_collection.update_one(filter, new_values, upsert=True)
            log("[+] Saved room list to MongoDB")

    def __restore(self) -> bool:
        """Restore a RoomList instance from  MongoDB. Find the record using the list_name as key, and populate
        list_name, create / modify times. Then set the object properties to the retrieved values and restore all 
        ChatRoom objects using the stored metadata
        
        Args:
            list_name (str): Unique identifier for the room_id that help identify it in the DB
        Returns:
            bool: Return true if RoomList object is restored successfully from the DB
        """
        metadata = self.__mongo_collection.find_one({'list_name': {'$exists': 'true'}})
        if metadata is None:
            log("[*] No metadata found for RoomList object", 'e')
            return False
        self.__list_name = metadata['list_name']
        self.__create_time = metadata['create_time']
        self.__modify_time = metadata['modify_time']
        self.__room_list = [ ChatRoom(
                                room_metadata['room_name'], 
                                room_metadata['room_type'], 
                                room_metadata['owner_alias'], 
                                room_metadata['member_list']) 
                            for room_metadata in metadata['rooms_metadata']]

    def is_room_declared(self, room_name: str) -> bool:
        """
        Check if room is declared in the room list

        Args:
            room_name (str): Room name to check existance of
        Returns:
            bool: Return true if the room is declared in the room list
        """
        log(f"[*] Starting search for room {room_name} in declared chat rooms")
        if self.length == 0:
            log(f"[*] No rooms are declared with the name {room_name}")
            return False

        for room in self.room_list:
            if room.room_name == room_name:
                log(f"[+] Found room {room_name} in declared chat rooms")
                return True

        log(f"[-] Could not find room {room_name} in declared chat rooms")
        return False

    def add(self, new_room: ChatRoom) -> bool:
        """
        Declare a new room to the room list

        Args:
            new_room (ChatRoom): ChatRoom implementation
        Returns:
            bool: True if the room is successfully added into the room 
            list, false otherwise
        """
        if self.is_room_declared(new_room.room_name):
            log(f"[*] Room is aready declared in roomlist {new_room}")
            return False
        else:
            self.room_list.append(new_room)
            self.__modify_time = datetime.now()
            log(f"[+] Added room {new_room.room_name} to room list")
            self.__persist()
            return True

    def remove(self, room_name: str) -> bool:
        """Remove a declared ChatRoom from the room list

        Args:
            room_name (str): Key name of the room that should be removed from the list
        Returns:
            bool: Return true if the room is successfully removed from the 
            roomlist, false otherwise
        """
        if self.is_room_declared(room_name):
            self.room_list.remove(room_name)
            self.__modify_time = datetime.now()
            log(f"[-] Removed room {room_name} from room list")
            return True
        else:
            log("[*] Room is not declared in room list")
            return False

    def find(self, room_name: str) -> ChatRoom | None:
        """
        Find a room in the room list and return it

        Args:
            room_name (str): Room name to search for in the room list

        Returns:
            ChatRoom: Chat room object in the room list
        """
        if room_name in self.room_list:
            return self.room_list[room_name]
        else:
            log("[*] Room is not declared in room list")
            return None

    def to_dict(self) -> dict:
        return {
            "list_name": self.list_name,
            "create_time": self.__create_time,
            "modify_time": self.__modify_time,
            "rooms_metadata": [room.metadata() for room in self.__room_list]
        }

    def __str__(self) -> str:
        room_list = ""
        for chat_room in self.room_list:
            room_list += chat_room.room_name + " "
        result = f"Room List({room_list})"
        return result
