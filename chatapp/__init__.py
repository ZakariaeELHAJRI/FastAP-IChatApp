from fastapi import FastAPI, Depends, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from chatapp.routers import user, message, friendships, authentication, conversation
from chatapp.auth import auth
from dotenv import load_dotenv
from chatapp.database import get_db
from dependencies.auth import get_current_user
from chatapp.models import User
from starlette.websockets import WebSocketDisconnect
from typing import List, Dict
import json

load_dotenv()

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
    allow_methods=["*"],  # You can specify specific HTTP methods (e.g., ["GET", "POST"])
    allow_headers=["*"],  # You can specify specific HTTP headers
)




# Define routes for CRUD operations
app.include_router(authentication.router, tags=["authentication"])
app.include_router(auth.auth_router, prefix="/api", tags=["auth"])
app.include_router(user.router, prefix="/api", tags=["users"])
app.include_router(message.router, prefix="/api", tags=["messages"])
app.include_router(friendships.router, prefix="/api", tags=["friendships"])
app.include_router(conversation.router, prefix="/api", tags=["conversations"])

@app.get("/")
async def root(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return {"message": "Hello World", "username": current_user.username}


# WebSocket connections
connected_clients: List[WebSocket] = []


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int, db: Session = Depends(get_db)):
    await websocket.accept()
    connected_clients.append(websocket)

    try:
        while True:
            message = await websocket.receive_text()
            # Handle received messages and update the database as needed
            # Emit WebSocket events to notify other connected clients
            await broadcast_message(user_id, message)
    except WebSocketDisconnect:
        connected_clients.remove(websocket)

async def broadcast_message(user_id: int, message_content: str):
    # Construct the message payload
    payload = {
        "user_id": user_id,
        "message": message_content,
    }

    # Convert the payload to JSON
    payload_json = json.dumps(payload)

    # Broadcast the message to all connected clients
    for client in connected_clients:
        await client.send_text(payload_json)
