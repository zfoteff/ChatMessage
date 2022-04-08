"""
API for the message chat application
"""

__author__ = "Zac Foteff"
__version__ = "2.0.0."

import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
from src.chat_room import ChatRoom
from src.room_list import RoomList
from src.user_list import UserList
from bin.constants import *
from bin.logger import Logger

app = FastAPI()
log = Logger("api")
log("[-+-] Started chat app")


@app.get("/", status_code=200)
async def index():
    """ Root endpoint for browser navigation to http://localhost:8000/

    Returns:
        dict: JSON(ish) response that can be viewed in the browser to confirm
        the website is running
    """
    start_time = time.perf_counter()
    elapsed_time = time.perf_counter() - start_time
    log(f"GET / {elapsed_time} result: Success")
    return JSONResponse(status_code=200, content="You've hit Zac's root endpoint!")


@app.post("/message/", status_code=201)
async def send_message(room_name: str, message: str, from_alias: str, to_alias: str):
    """ API endpoint for sending message to the chat application

    Args:
        room_name (str): room name to send message to
        message (str): message payload to send to room
        from_alias (str): sender alias
        to_alias (str): reciever alias
    Returns:
        JSONResponse: status of sent message user can view in the browser
    """
    start_time = time.perf_counter()
    chat_room = ChatRoom(room_name=room_name)
    chat_room.send_message(message=message, room_name=room_name, from_alias=from_alias, to_alias=to_alias)
    elapsed_time = time.perf_counter() - start_time
    log(f"POST /message/ {elapsed_time} result: Success")
    return JSONResponse(status_code=201, content='Enqueued message')


@app.get('/messages/', status_code=200)
async def get_messages(request: Request, alias: str, room_name: str, messages_to_get: int = GET_ALL_MESSAGES):
    """ Message retrieval endpoint for the application

    Args:
        request (Request): 
        alias (str): 
        room_name (str): 
        messages_to_get (int, optional): 
    Returns:
        dict: JSON(ish) response so the user can view all the messages in the browser
    """
    log(f"Attempting to send messages to chat room {room_name} . . .")
    start_time = time.perf_counter()
    chat_room = ChatRoom(room_name=room_name)
    messages = chat_room.get_messages(alias)
    elapsed_time = time.perf_counter() - start_time
    log(f"GET /messages/ {elapsed_time} result: Success")
    return JSONResponse(status_code=200, content=messages)

"""
User routes
"""
@app.get('/users/', status_code=200)
async def get_users(list_name: str=DB_DEFAULT_USER_LIST):
    """
    """
    start_time = time.perf_counter()
    users = UserList(list_name=list_name)
    if len(users.get_all_users()) > 0:
        elapsed_time = time.perf_counter() - start_time
        log(f"GET /users/ {elapsed_time} result: 200")
        return JSONResponse(status_code=200, content=users.get_all_users())
    else:
        elapsed_time = time.perf_counter() - start_time
        log(f"GET /users/ {elapsed_time} result: 405")
        return JSONResponse(status_code=405, content="No users registered")

@app.post('/register/user/', status_code=201)
async def register_user(user_alias: str):
    """Register a new user to to the User List
    """
    start_time = time.perf_counter()
    users = UserList()
    users.register(user_alias)
    elapsed_time = time.perf_counter() - start_time
    users.register(new_alias=user_alias)
    log(f"POST /register/user/ {elapsed_time} result: 201")
    return JSONResponse(status_code=201, content="Success")

"""
Room routes
"""
@app.post("/room/", status_code=201)
async def create_room(room_name: str, owner_alias: str, room_type: int = CHAT_ROOM_TYPE_PUBLIC):
    """API endpoint for creating a room

    Args:
        room_name (str): _description_
        owner_alias (str): _description_
        room_type (int, optional): _description_. Defaults to CHAT_ROOM_TYPE_PUBLIC.
    """
    start_time = time.perf_counter()
    log(f"Creating a new room with the name {room_name}")
    room_list = RoomList()
    new_room = ChatRoom(room_name=room_name, room_type=room_type, owner_alias=owner_alias)
    if room_list.add(new_room):
        elapsed_time = time.perf_counter() - start_time
        log(f"POST /room/{room_name}/{owner_alias}/{room_type} {elapsed_time} result: Success")
        return JSONResponse(status_code=201, content="Successfully created new room")
    else:
        elapsed_time = time.perf_counter() - start_time
        log(f"POST /room/{room_name}/{owner_alias}/{room_type} {elapsed_time} result: Room already exists")
        return JSONResponse(status_code=405, content="Room not created")
