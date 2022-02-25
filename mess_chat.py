from fastapi import FastAPI
from rmq import RMQMessageInteractions
from bin.logger import Logger

rmq = RMQMessageInteractions()
app = FastAPI()
chat_log = Logger("api")
chat_log("[-+-] Started chat app")

@app.get("/")
async def root():
    """ Root endpoint for browser navigation to http://localhost:8000/

    Returns:
        dict: JSON(ish) response that can be viewed in the browser to confirm
        the website is running
    """
    chat_log(f"GET / -- result: Success")
    return {'message': "You've hit Zac's API root endpoint"}

@app.post("/send/")
async def send(room_name: str, message: str, from_alias: str, to_alias: str, group_room: bool):
    """ Send endpoint for the application. 

    Args:
        room_name (str): room name to send message to
        message (str): message payload to send to room
        from_alias (str): sender alias
        to_alias (str): reciever alias
        group_room (bool): Flag indicating if room is a group room

    Returns:
        dict: JSON(ish) status of sent message user can view in the browser
    """
    result = rmq.sendMessage(message)
    chat_log(f"POST /send/ -- result: ENQUEUED")
    return result
    
@app.get('/messages/')
async def messages():
    """ Message retrieval endpoint for the application

    Returns:
        dict: JSON(ish) response so the user can view all the messages in the browser
    """
    results = rmq.recieveMessages()
    chat_log(f"GET /messages/ -- result: {results}")
    return results