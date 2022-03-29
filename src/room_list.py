""" 
Room list dequeue implementation for managing declared channels on the 
messaging service
"""

__author__= "Zac Foteff"
__version__ =  "1.0.0."

from pymongo import MongoClient
from datetime import datetime
from bin.constants import *
from bin.logger import Logger
from src.chat_room import ChatRoom

log = Logger()

class RoomList:
    """
    RoomList object class that stores all declared ChatRoom instances 
    """
    def __init__(self, room_id: str=DEFAULT_ROOM_LIST_ID) -> None:
        """
        Stores rooms in a list of dict of with the room name acting as 
        the key and the ChatRoom instance and a dirty flag as values. Should ensure 
        that if no room list is passed to the constructor, then the application 
        will try to restore a room list, or create a new list if no room list 
        is already stored in the database
        """
        #   Initialize MongoDB resources
        self.__mongo_client = MongoClient(DB_HOST)
        self.__mongo_db = self.__mongo_client.gufoteff
        self.__mongo_collection = self.__mongo_db.get_collection('room_list')
        if self.__mongo_collection is None:
            #   Initialize the chat queue collection in the DB if it does not already exist
            self.__mongo_collection = self.__mongo_db.create_collection("room_list")
        
        if self.__restore(room_id):
            self.__dirty = False
        else:
            self.__room_id = room_id
            self.__room_list = []
            self.__dirty = True
            self.__create_time = datetime.now()
            self.__modify_time = datetime.now()
        
    @property
    def room_id(self) -> str:
        return self.__room_id

    @property
    def room_list(self) -> list:
        return self.__room_list

    @property
    def dirty(self) -> bool:
        return self.__dirty

    @property
    def length(self) -> int:
        return len(self.__room_list)
        
    def __persist(self) -> bool:
        """Persist a RoomList instance in  MongoDB. Create document using the ChatRoom instance room name
        as a key, then restore the ChatRoom instances that are declared for this instance of the application. Uses
        the update_one collection to minimize the amount of objects that are stored in the DB. Elements are selected
        using their unique room id.
        NOTE: the updaate_one method is used with the upsert flag raised to tell the system to create a new object if
        the object does not already exist in the DB
        """
        if self.dirty:
            log(f"[*] Persisting {self} to MongoDB")
            new_values = { 
                "$set": {
                    "room_id": self.room_id,
                    "room_list": self.room_list,
                    "create_time": self.__create_time,
                    "modify_time": self.__modify_time
                }}
            self.__mongo_collection.update_one(
                {'room_id': self.room_id}, 
                new_values, 
                upsert=True)
            log(f"[+] Persisted {self} to MongoDB")
            return True
        else:
            log("[-] Room List is not flagged as dirty, but persist was called. Cancelling operation . . .", 'w')
            return False
    
    def __restore(self, room_id: str) -> bool:
        """Restore a RoomList instance from  MongoDB
        Args:
            room_id (str): Unique identifier for the room_id that helsp identify it in the DB
        Returns:
            bool: Return true if RoomList object is restored successfully from the DB
        """
        pass
    
    @property
    def room_list(self) -> dict:
        return self.__room_list
    
    def is_room_declared(self, room_name: str) -> bool:
        """
        Check if room is declared in the room list

        Args:
            room_name (str): Room name to check existance of
        Returns:
            bool: Return true if the room is declared in the room list
        """
        log(f"[*] Starting search for room {room_name} in declared chat rooms")
        if (self.length == 0):
            log("[*] No rooms are declared. Cancelling operation . . .")
            return False

        for room_metadata in self.room_list:
            if room_metadata['room_name'] == room_name:
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
            self.room_list[new_room.room_name] = new_room
            log(f"[+] Added room {new_room.room_name} to roomlist {new_room}")
            self.room_list[new_room.room_name].dirty = True
            self.dirty = True
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
            self.room_list.pop(room_name)
            log(f"[-] Removed room {room_name} from roomlist")
            return True
        else:
            log("[*] Room is not declared in roomlist")
            return False
        
    def find(self, room_name: str) -> ChatRoom:
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
            log("[*] Room is not declared in roomlist")
            return None

    def to_dict(self) -> str:
        return {
            "room_id": self.room_id,
            "room_list": self.room_list,
            "dirty": self.dirty,
            "create_time": self.__create_time,
            "modify_time": self.__modify_time
        }

    def __str__(self) -> str:
        room_list = ""
        for chat_room in self.room_list:
            room_list += chat_room.room_name + " "
        result = f"Room List({room_list})"
        return result

