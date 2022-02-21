from fastapi import FastAPI
from rmq import RMQMessageInteractions
from logger import Logger

rmq = RMQMessageInteractions()
app = FastAPI()
chat_log = Logger("chat")
chat_log("[-+-] Started chat app")
    
@app.on_event("shutdown")
def shutdown_event():
    rmq.close()
    chat_log("[-X-] Shutdown chat app")

@app.get("/")
async def root():
    """
    Root endpoint for browser navigation to http://localhost:8000/

    Returns:
        dict: JSON(ish) response that can be viewed in the browser to confirm
        the website is running
    """
    chat_log(f"GET / -- result: Success")
    return {'message': "You've hit Zac's API root endpoint"}

@app.post("/send/")
async def send(message: str):
    """
    Send endpoint for the application. 

    Args:
        message (str): Message to send to RMQ server

    Returns:
       dict: JSON(ish) response that can be viewed in browser to 
       confirm the message was enqueued
    """
    result = rmq.sendMessage(message)
    chat_log(f"POST /send/ -- result: ENQUEUED")
    return result
    
@app.get('/messages/')
async def messages():
    """
    Message retrieval endpoint for the application

    Returns:
        dict: JSON(ish) response so the user can view all the messages in the browser
    """
    results = rmq.recieveMessages()
    chat_log(f"GET /messages/ -- result: {results}")
    return results