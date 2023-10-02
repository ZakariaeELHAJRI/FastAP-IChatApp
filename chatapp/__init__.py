from fastapi import FastAPI, WebSocket, Depends, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from chatapp.routers import user, message, friendships, authentication, conversation , notification
from chatapp.crud.message import create_new_message
from chatapp.crud.notification import create_notification
from chatapp.auth import auth
from dotenv import load_dotenv
from chatapp.database import get_db
from dependencies.auth import get_current_user_websocket
from chatapp.crud.friendships import create_friendship
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

    async def send_message(self, receiver_id: int,sender_id: int , invitation_data: Dict):
        receiver_id_str = str(receiver_id)  # Convert receiver_id to a string
        sender_id_str = str(sender_id)
        print("connections:", self.connections)
        if receiver_id_str in self.connections:
            print("Sending message to user", receiver_id)
            await self.connections[receiver_id_str].send_json(invitation_data)
        else:
            print("User", receiver_id, "is not connected")
        
        if sender_id_str in self.connections:
            print("Sending message to user", sender_id)
            await self.connections[sender_id_str].send_json(invitation_data)
        else:
            print("User", sender_id, "is not connected")


    async def send_invitation(self, receiver_id: int, invitation_data: Dict):
        receiver_id_str = str(receiver_id)
        if receiver_id_str in self.connections:
            print("Sending invitation to user", receiver_id)
            await self.connections[receiver_id_str].send_json(invitation_data)
        else:
            print("User", receiver_id, "is not connected")
    async def send_accepation(self, user1_id: int, invitation_data: Dict):
        user1_id_str = str(user1_id)
        if user1_id_str in self.connections:
            print("Sending acceptance to user", user1_id)
            await self.connections[user1_id_str].send_json(invitation_data)
        else:
            print("User", user1_id, "is not connected")
    async def new_conversation(self, receiver_id: int,sender_id: int , invitation_data: Dict):
        receiver_id_str = str(receiver_id)
        sender_id_str = str(sender_id)
        if receiver_id_str in self.connections:
            print("Sending message to user", receiver_id)
            await self.connections[receiver_id_str].send_json(invitation_data)
        else:
            print("User", receiver_id, "is not connected")
        
        if sender_id_str in self.connections:
            print("Sending message to user", sender_id)
            await self.connections[sender_id_str].send_json(invitation_data)
        
    async def broadcast_invitation(self, invitation_data: Dict):
        # Loop through all connected clients and send the invitation
        for user_id, websocket in self.connections.items():
            await websocket.send_json(invitation_data)

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
app.include_router(notification.router, prefix="/api", tags=["notifications"])

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
            data_str = await websocket.receive_text()
            data = json.loads(data_str)
            event_name = data.get("event")

            if event_name == "message":
                print("data from client:", data)
                content = data['data'].get("content")
                sender_id = data['data'].get("sender_id")
                receiver_id = data['data'].get("receiver_id")
                time = data['data'].get("time")
                conversation_id = data['data'].get("conversation_id")
                is_read = data['data'].get("is_read")

                new_message_data = {
                    "content": content,
                    "sender_id": sender_id,
                    "receiver_id": receiver_id,
                    "time": time,
                    "conversation_id": conversation_id,
                    "is_read": is_read,
                    "event": "message"
                }
                print("New message:", new_message_data)
                await websocket_consumer.send_message(int(receiver_id),int(sender_id), new_message_data)
                create_new_message(new_message_data, current_user, db)
                print("The message has been sent to the recipient")

            elif event_name == "invitation":
                print("data from client:", data)
                sender_id = data['data'].get("user_id")
                receiver_id = data['data'].get("friend_id")
                user_name = data['data'].get("user_name")

                new_invitation_data_socket = {
                    "sender_id": sender_id,
                    "receiver_id": receiver_id,
                    "status": "pending" ,
                    "user_name": user_name,
                    "is_read": False,
                    "event": "invitation"
                    
                }
                invitation_data =  {
                    "user_id": sender_id,
                    "friend_id": receiver_id,
                    "status": "pending",
                    "is_read": False,
                    "event": "invitation"
                }
                print("New invitation:", invitation_data)
                await websocket_consumer.send_invitation(int(receiver_id), new_invitation_data_socket)
                create_friendship(db, invitation_data)
                print("The invitation has been sent to the recipient")
            
            elif event_name == "acceptance":
                
                user1_id = data['data'].get("user_id")
                user2_id = data['data'].get("friend_id")

                new_acceptance_data_socket = {
                    "user1_id": user1_id,
                    "user2_id": user2_id,
                    "status": "accepted",
                    "event": "acceptance"
                }
                notification_data = {
                    "sender_id": user2_id,
                    "recipient_id": user1_id,
                    "message": "accepte your invitation",
                   
                }
                print("New acceptance:", new_acceptance_data_socket)
                await websocket_consumer.send_accepation(int(user1_id), new_acceptance_data_socket)
                create_notification(db, notification_data)
                print("The acceptance has been sent to the recipient")
            elif event_name == "newConversation":
                user1_id = data['data'].get("user1_id")
                user2_id = data['data'].get("user2_id")
                print('data new conversation:', data)

                new_conversation_data_socket = {
                    "user1_id": user1_id,
                    "user2_id": user2_id,
                    "event": "newConversation"
                }
                print("New conversation:", new_conversation_data_socket)
                await websocket_consumer.new_conversation(int(user1_id),int(user2_id), new_conversation_data_socket)
                print("The conversation has been sent to the recipient")

    except WebSocketDisconnect:
        websocket_consumer.disconnect(str(user_id))
    except Exception as e:
        print(f"WebSocket Error: {str(e)}")
