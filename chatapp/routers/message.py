from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from chatapp.crud.message import create_message, get_message, get_messages , update_message, delete_message
from chatapp.database import get_db
from chatapp.models.message import Message
from dependencies.auth import User, get_current_user
router = APIRouter()

@router.post("/messages/")
def create_new_message(message_data: dict, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    sender_id = current_user.id  # Get the sender's user ID from the authenticated user
    receiver_id = message_data.get("receiver_id")  # Assuming you have a "receiver_id" field in the message_data
    conversation_id = message_data.get("conversation_id")  # Assuming you have a "conversation_id" field in the message_data

    try:
        # Check if 'receiver_id' and 'conversation_id' are valid and belong to the second user
        receiver = db.query(User).filter(User.id == receiver_id).first()
        if not receiver:
            raise ValueError("Invalid receiver.")

        # Remove 'sender_id' from 'message_data'
        if 'sender_id' in message_data:
            del message_data['sender_id']

        message = create_message(db, message_data, sender_id, receiver_id, conversation_id)
        return message
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))




@router.get("/messages/{message_id}")
def get_single_message(message_id: int,current_user: User = Depends(get_current_user),  db: Session = Depends(get_db)):
    message = get_message(db, message_id)
    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return message

@router.get("/messages/")
def get_all_messages(skip: int = 0, limit: int = 10,current_user: User = Depends(get_current_user),  db: Session = Depends(get_db)):
    return get_messages(db, skip, limit)

@router.put("/messages/{message_id}")
def update_existing_message(message_id: int, message_data: dict,current_user: User = Depends(get_current_user),  db: Session = Depends(get_db)):
    message = update_message(db, message_id, message_data)
    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return message

@router.delete("/messages/{message_id}")
def delete_existing_message(message_id: int,current_user: User = Depends(get_current_user),  db: Session = Depends(get_db)):
    message = delete_message(db, message_id)
    if message is False:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"message": "Message deleted successfully"}

def get_messages_by_user(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Message).filter(Message.user_id == user_id).all()


