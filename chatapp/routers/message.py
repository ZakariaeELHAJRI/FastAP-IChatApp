from fastapi import APIRouter, Depends, HTTPException  , WebSocket , WebSocketDisconnect 
from sqlalchemy.orm import Session 
from chatapp.crud.message import  get_message, get_messages, get_messages_by_conversation , update_message, delete_message ,create_new_message 
from chatapp.crud.conversation import get_conversation
from chatapp.database import get_db
from chatapp.models.message import Message 
from dependencies.auth import User, get_current_user
import logging
router = APIRouter()

   
@router.post("/messages/")
async def create_message_endpoint(
    message_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    created_message = create_new_message(message_data, current_user, db)
    return created_message

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

@router.put("/mark-messages-as-read/{conversation_id}")
def mark_messages_as_read(conversation_id: int,current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        conversation = get_conversation(db, conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        messages = get_messages_by_conversation(db,conversation_id)
    # Check if the conversation has messages
        if messages:
                # Mark only unread messages in the conversation as read
                for message in messages:
                    if not message.is_read and message.receiver_id==current_user.id :
                        message.is_read = True

                db.commit()
                db.refresh(conversation)

        return conversation

    except Exception as e:
        logging.error(f"Error in mark_messages_as_read: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/messages/{message_id}")
def delete_existing_message(message_id: int,current_user: User = Depends(get_current_user),  db: Session = Depends(get_db)):
    message = delete_message(db, message_id)
    if message is False:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"message": "Message deleted successfully"}

def get_messages_by_user(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Message).filter(Message.user_id == user_id).all()


