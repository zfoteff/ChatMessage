# ChatMessage
Chat Message Application during lab 3 of CPSC 313 at Gonzaga University, and expanded upon in further assignments.

Dependancies:
* pika
* requests
* pytest
* fastapi
* logging

This uses the ChatMessageEnv virtual environment for development
To Run
```bash
ChatMessageEnv/Scripts/Activate.ps1
```

Docker Image for local testing

```bash
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

To run:

```bash
python -m uvicorn mess_chat:app --reload
```

This will run the application on <http://localhost:8000/>. The endpoints are ./send/{message} to send messages to the server and ./messages/ to retrieve the messages.
