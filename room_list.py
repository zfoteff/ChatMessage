""" 
Room list dequeue implementation for managing declared channels on the 
messaging service
"""

__author__= "Zac Foteff"
__version__ =  "1.0.0."

from importlib.metadata import metadata
from pymongo import MongoClient
from datetime import datetime
from bin.constants import DB_HOST
from bin.logger import Logger
from chat_room import ChatRoom

log = Logger()

class RoomList:
    """
    RoomList object class that stores all declared ChatRoom instances 
    """
    def __init__(self) -> None:
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
        self.__mongo_colleciton = self.__mongo_db.get_collection('room_list')
        if self.__mongo_collection is None:
            #   Initialize the chat queue collection in the DB if it does not already exist
            self.__mongo_collection = self.__mongo_db.create_collection("room_list")
        
        if self.__restore():
            self.__dirty = False
        else:
            self.__room_list = []
            self.__dirty = True
            self.__create_time = datetime.now()
            self.__modify_time = datetime.now()
        
    @property
    def room_list(self) -> dict:
        return self.room_list

    @property
    def dirty(self) -> bool:
        return self.__dirty

    @property
    def length(self) -> int:
        return len(self.room_list)
        
    def __persist() -> bool:
        """Persist a RoomList instance in  MongoDB. Create document using the ChatRoom instance room name
        as a key, then restore the ChatRoom instances that are declared for this instance of the application.
        """
        if self.dirty:
            pass
        else:
            log("[-] Room List is not flagged as dirty, but persist was called. Cancelling operation . . .", 'w')
            return False
    
    def __restore() -> bool:
        """Restore a RoomList instance from  MongoDB
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
        if (self.length == 0)

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
            room_metadata = {
                "room_name": new_room.room_name,
                "room_obj": new_room.to_dict,
                "dirty": True
            }
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

    def __str__(self) -> str:
        room_list = ""
        for chat_room in self.room_list
        result = f"Room List({room_list})"
        return result
