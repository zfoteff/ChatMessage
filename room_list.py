""" 
Room list dequeue implementation for managing declared channels on the 
messaging service
"""

__author__= "Zac Foteff"
__version__ =  "1.0.0."

from db_helper import ChatRoomDBHelper
from bin.logger import Logger
from chat_room import ChatRoom

logger = Logger()

class RoomList:
    """
    RoomList object class
    """
    def __init__(self, room_list: dict=None):
        """
        Stores rooms in a list of key-value pairs with the room name 
        acting as the key. Should ensure that if no room list is passed to the 
        constructor, then the application will try to restore a room list, or 
        create a new list if no room list is already stored in the database
        """

        self.__room_list = {}
        self.__db_helper = ChatRoomDBHelper()
        
    def __persist():
        """Persist a RoomList instance in the MongoDB
        """
        pass
    
    def __restore():
        """Restore a RoomList instance from the MongoDB
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
        return room_name in self.room_list.keys()
        
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
            logger(f"[*] Room is aready declared in roomlist {new_room}")
            return False
        else:
            self.room_list[new_room.room_name] = ChatRoom
            logger(f"[+] Added room {new_room.room_name} to roomlist {new_room}")
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
            logger(f"[-] Removed room {room_name} from roomlist")
            return True
        else:
            logger("[*] Room is not declared in roomlist")
            return False
        
    def find(self, room_name: str) -> ChatRoom:
        """
        Find a room in the room list and return it

        Args:
            room_name (str): Room name to search for in the room list

        Returns:
            ChatRoom: Chat room object in the room list
        """
        if self.room_list.keys().__contains__(room_name):
            return self.room_list[room_name]
        else:
            logger("[*] Room is not declared in roomlist")
            return None