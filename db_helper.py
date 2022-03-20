"""
MongoDB database interaction helper file. Will be used in future to encapsulate all database interactions 
into one file

@author Zac Foteff
@version 1.0.0.
"""

import pymongo
from bin.logger import Logger
from bin.constants import *

class ChatRoomDBHelper():
    def __init__(self, db_name: str=DB_NAME, collection: str=DB_COLLECTION):
        self.client = pymongo.MongoClient(DB_HOST, DB_PORT)
        self.db = self.client[db_name]
        self.collection = collection
        
    @property
    def collection(self):
        return self.colletion
        
    def insert(self):
        """Insert object into database as a new document
        """
        pass
    
    def remove(self):
        """Remove object's document from the database
        """
        pass
    
    def find(self):
        """_summary_
        """
        pass

ChatMessageDBHelper()