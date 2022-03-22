"""
API for the message chat application

@author Zac Foteff
@version 2.0.0.
"""

import socket
import datetime
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, ORJSONResponse, Response
from bin.constants import *
from bin.logger import Logger
from chat_room import ChatRoom
from message_props import MessageProperties
from chat_message import ChatMessage

app = FastAPI()
log = Logger("api")
log("[-+-] Started chat app")
ip_address = ""
user = ""

@app.get("/", status_code=200)
async def root():
    """ Root endpoint for browser navigation to http://localhost:8000/

    Returns:
        dict: JSON(ish) response that can be viewed in the browser to confirm
        the website is running
    """
    log(f"GET / -- result: Success")
    return {'message': "You've hit Zac's API root endpoint"}

@app.post("/send/", status_code=201)
async def send(room_name: str, message: str, from_alias: str, to_alias: str):
    """ Send endpoint for the application

    Args:
        room_name (str): room name to send message to
        message (str): message payload to send to room
        from_alias (str): sender alias
        to_alias (str): reciever alias
        group_room (bool): Flag indicating if room is a group room

    Returns:
        dict: JSON(ish) status of sent message user can view in the browser
    """
    chat_room = ChatRoom(room_name=room_name, exchange_name=room_name)
    mess_props = MessageProperties(MESSAGE_SENT, room_name, to_alias, from_alias)
    if chat_room.send_message(message=message, mess_props=mess_props) is True:
        return JSONResponse(status_code=201, content={'result': 'ENQUEUED'})
    else:
        return JSONResponse(status_code=410, content="Problems")

@app.post("/create/room")
async def create_room(room_name: str, owner_alias: str, room_type: int=CHAT_ROOM_TYPE_PUBLIC):
    """Create a new chat room and add it to the RoomList

    Args:
        room_name (str): _description_
        owner_alias (str): _description_
        room_type (int, optional): _description_. Defaults to CHAT_ROOM_TYPE_PUBLIC.
    Returns:
        _type_: _description_
    """
    
    
@app.get('/messages/', status_code=200)
async def messages(req: Request, alias: str, exchange_name: str, group_queue: bool=True, messages_to_get: int=GET_ALL_MESSAGES):
    """ Message retrieval endpoint for the application

    Returns:
        dict: JSON(ish) response so the user can view all the messages in the browser
    """
    log("[*] Attemping to retrieve messages from chat room . . .")
    if (queue_instance := ChatRoom(exchange_name, room_name=alias, group_queue=group_queue)) is None:
        log("[-] Chat room does not exist. Aborting . . . ", 'e')
        return JSONResponse(status_code=415, content=f'Chat queue {exchange_name} does not exist.')
    messages, num_messages = queue_instance.get_messages(num_messages=messages_to_get)
    for message in messages:
        log(f"{message.message}{message.mess_props}")
    return messages

def main():
    ip_address = socket.gethostbyname(socket.gethostname())
    user = input("Please enter your name: ")
    log(f"[+] User {user} logged in at {ip_address}")

if __name__ == '__main__':
    main()