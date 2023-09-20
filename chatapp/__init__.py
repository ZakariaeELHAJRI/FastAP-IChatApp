from fastapi import FastAPI, WebSocket, Depends, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from chatapp.routers import user, message, friendships, authentication, conversation
from chatapp.crud.message import create_new_message
from chatapp.auth import auth
from dotenv import load_dotenv
from chatapp.database import get_db
from dependencies.auth import get_current_user_websocket
import asyncio
import json
from typing import Dict


load_dotenv()

class WebSocketConsumer:
    def __init__(self):
        self.connections = {}  # Dictionary to store WebSocket connections

    async def connect(self, websocket, user_id):
        await websocket.accept()
        self.connections[user_id] = websocket

    def disconnect(self, user_id):
        if user_id in self.connections:
            del self.connections[user_id]

    async def send_message(self, receiver_id: int, message_data: Dict):
        receiver_id_str = str(receiver_id)  # Convert receiver_id to a string
        print("connections:", self.connections)
        if receiver_id_str in self.connections:
            print("Sending message to user", receiver_id)
            await self.connections[receiver_id_str].send_json(message_data)
        else:
            print("User", receiver_id, "is not connected")

# Create an instance of WebSocketConsumer
websocket_consumer = WebSocketConsumer()

app = FastAPI()

# Configure CORS settings
origins = [
    "http://localhost:3000",  # Add the URL of your Next.js frontend
    "http://localhost:8000",  # Add the URL of your FastAPI server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define routes for CRUD operations (include your existing routes)
app.include_router(authentication.router, tags=["authentication"])
app.include_router(auth.auth_router, prefix="/api", tags=["auth"])
app.include_router(user.router, prefix="/api", tags=["users"])
app.include_router(message.router, prefix="/api", tags=["messages"])
app.include_router(friendships.router, prefix="/api", tags=["friendships"])
app.include_router(conversation.router, prefix="/api", tags=["conversations"])

# Define a custom dependency function that combines get_current_user and get_db
def get_current_user_and_db(websocket: WebSocket, db: Session = Depends(get_db)):
    current_user = websocket.get('current_user')
    return current_user, db

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int, token: str = Query(...), db: Session = Depends(get_db)):
    current_user = await get_current_user_websocket(token, db)
    
    if not current_user:
        await websocket.close()
        return

    await websocket_consumer.connect(websocket, str(user_id))
    try:
        while True:
            # Receive messages from the client
            message_data_str = await websocket.receive_text()
            message_data = json.loads(message_data_str)
            event_name = message_data.get("event")

            if event_name == "message":
                content = message_data.get("content")
                sender_id = message_data.get("sender_id")
                receiver_id = message_data.get("receiver_id")
                time = message_data.get("time")
                conversation_id = message_data.get("conversation_id")

                new_message_data = {
                    "content": content,
                    "sender_id": sender_id,
                    "receiver_id": receiver_id,
                    "time": time,
                    "conversation_id": conversation_id
                }

                await websocket_consumer.send_message(int(receiver_id), new_message_data)
                create_new_message(new_message_data, current_user, db)
                print("The message has been sent to the recipient")

    except WebSocketDisconnect:
        websocket_consumer.disconnect(str(user_id))
    except Exception as e:
        print(f"WebSocket Error: {str(e)}")
