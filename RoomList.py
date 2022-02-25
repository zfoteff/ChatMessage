"""

"""

from bin.logger import Logger
from ChatRoom import ChatRoom

logger = Logger()

class RoomList:
    def __persist():
        pass
    
    def __restore():
        pass
    
    def __init__(self):
        """Stores rooms in a list of key-value pairs with the room name 
        acting as the key
        """
        self.name = ""
        self.room_list = {}
        
    @property
    def name(self):
        return self.name
        
    def add(self, new_room: ChatRoom):
        if self.room_list.keys().__contains__(ChatRoom.room_name):
            logger(f"[*] Room is aready declared in roomlist {new_room}")
            return False
        else:
            self.room_list[new_room.room_name] = ChatRoom
            logger(f"[+] Added room {new_room.room_name} to roomlist {new_room}")
            return True
        
    def remove(self, room_name: str):
        if self.room_list.keys().__contains__(room_name):
            self.room_list.pop(room_name)
            logger(f"[-] Removed room {room_name} from roomlist")
            return True
        else:
            logger("[*] Room is not declared in roomlist")
            return False
        
    def find(self, room_name):
        if self.room_list.keys().__contains__(room_name):
            return self.room_list[room_name]
        else:
            logger("[*] Room is not declared in roomlist")
            return None