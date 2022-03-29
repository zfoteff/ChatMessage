"""Constants file for Chat application"""

__author__ = "Zac Foteff"
__version__ = "1.0.0."

#   MongoDB Constants
DB_HOST = '34.94.157.136'
DB_PORT = 27017
DB_USER = "class"
DB_PASS = "CPSC313"
DB_AUTH_SOURCE = "cpsc313"
DB_NAME = "cpsc313"
DB_ROOM_LIST_COLLECTION = 'rooms'
DB_USER_LIST_COLLECTION = 'users'
DB_DEFAULT_ROOM_LIST = 'main'
DB_DEFAULT_USER_LIST = 'global'

#   RMQ Constants
RMQ_DEV_HOST = "localhost"
RMQ_PROD_HOST = "35.236.51.203"
RMQ_PORT = 5672
RMQ_DEFAULT_EXCHANGE_TYPE = "fanout"
RMQ_USER = "class"
RMQ_PASS = "CPSC313"
RMQ_DEFAULT_PUBLIC_QUEUE = "general"
RMQ_DEFAULT_PUBLIC_EXCHANGE = ""
RMQ_PRIVATE_QUEUE = "foteff"
GET_ALL_MESSAGES = -1
MESSAGE_RECEIVED = 1
MESSAGE_SENT = 0

#   ChatRoom Constants
CHAT_ROOM_TYPE_PUBLIC = 100
CHAT_ROOM_TYPE_PRIVATE = 200

#   RoomList Constants
DEFAULT_ROOM_LIST_ID = "roomlist_foteff"
