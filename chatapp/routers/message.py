from fastapi import APIRouter, Depends, HTTPException  , WebSocket , WebSocketDisconnect
from sqlalchemy.orm import Session
from chatapp.crud.message import  get_message, get_messages , update_message, delete_message ,create_new_message
from chatapp.database import get_db
from chatapp.models.message import Message
from dependencies.auth import User, get_current_user
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

@router.delete("/messages/{message_id}")
def delete_existing_message(message_id: int,current_user: User = Depends(get_current_user),  db: Session = Depends(get_db)):
    message = delete_message(db, message_id)
    if message is False:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"message": "Message deleted successfully"}

def get_messages_by_user(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Message).filter(Message.user_id == user_id).all()


