"""
MongoDB database interaction helper file

@author Zac Foteff
@version 1.0.0.
"""

import pymongo
from bin.logger import Logger

DB_HOST = '34.94.157.136'
DB_PORT = '5672'
DEFAULT_DB_NAME = ""
DEFAULT_COLLECTION_NAME = ""

class ChatRoomDBHelper():
    def __init__(self, db_name: str=DEFAULT_DB_NAME, collection: str=DEFAULT_COLLECTION_NAME):
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