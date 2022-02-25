"""

"""

from datetime import datetime
from bin.logger import Logger

logger = Logger("messageProperties")

MESSAGE_SENT = 0
MESSAGE_RECIEVED = 1

class MessageProperties:
    def __init__(self, sequence_number: int, 
                 id: int, 
                 mess_type: str, 
                 room_name: str, 
                 to_user: str, 
                 from_user: str,
                 sent_time: datetime,
                 rec_time: datetime):
        self.sequence_number = sequence_number
        self.id = id
        self.mess_type = mess_type
        self.room_name = room_name
        self.from_user = from_user
        self.to_user = to_user
        self.sent_time = sent_time
        self.rec_time = rec_time
        
    def __str__(self):
        return (f"\nMessage properties"
               +f"\n\tID: {self.id} Sequence number: {self.sequence_number}\n\t"
               +f"\n\tRoom: {self.room_name} Sender: {self.from_user} | {self.sent_time} Receiever: {self.to_user} | {self.rec_time}")