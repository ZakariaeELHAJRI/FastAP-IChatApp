from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from chatapp.crud.conversation import create_conversation, get_conversation, get_conversations , update_conversation, delete_conversation
from chatapp.database import get_db
from chatapp.models.conversation import Conversation
from chatapp.models.message import Message
from dependencies.auth import User, get_current_user
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from sqlalchemy import or_ , and_ 

router = APIRouter()

@router.post("/conversations/")
def create_new_conversation(conversation_data: dict, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    conversation = create_conversation(db, conversation_data)
    return conversation

@router.get("/conversations/{conversation_id}")
def get_single_conversation(conversation_id: int,current_user: User = Depends(get_current_user),  db: Session = Depends(get_db)):
    conversation = get_conversation(db, conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@router.get("/conversations/")
def get_all_conversations(skip: int = 0, limit: int = 10,current_user: User = Depends(get_current_user),  db: Session = Depends(get_db)):
    return get_conversations(db, skip, limit)

@router.put("/conversations/{conversation_id}")
def update_existing_conversation(conversation_id: int, conversation_data: dict,current_user: User = Depends(get_current_user),  db: Session = Depends(get_db)):
    conversation = update_conversation(db, conversation_id, conversation_data)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@router.delete("/conversations/{conversation_id}")
def delete_existing_conversation(conversation_id: int,current_user: User = Depends(get_current_user),  db: Session = Depends(get_db)):
    conversation = delete_conversation(db, conversation_id)
    if conversation is False:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"message": "Conversation deleted successfully"}

@router.get("/customconversations/", response_model=list[dict])
def get_conversations(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Get conversations where the current user is a participant
    conversations = (
        db.query(Conversation)
        .filter(or_(Conversation.user1_id == current_user.id, Conversation.user2_id == current_user.id))
        .all()
    )

    # Define a list to store conversation data
    conversation_data = []

    for conversation in conversations:
        # Determine the friend's ID based on the conversation
        friend_id = (
            conversation.user2_id if conversation.user1_id == current_user.id else conversation.user1_id
        )

        # Get the friend's name
        friend = db.query(User).filter(User.id == friend_id).first()
        friend_name = f"{friend.firstname} {friend.lastname}"

        # Get all messages in this conversation between the current user and their friend
        messages = (
            db.query(Message)
            .filter(Message.conversation_id == conversation.id)
            .filter(or_(
                and_(Message.sender_id == current_user.id, Message.receiver_id == friend_id),
                and_(Message.sender_id == friend_id, Message.receiver_id == current_user.id)
            ))
            .order_by(Message.send_at.asc())  # Order by message send time
            .all()
        )

        # Extract the message content and send time
        messages_data = [{
            "content": message.content,
            "time": message.send_at,
            "sender_id": message.sender_id,
        } for message in messages]

        # Get the last message in this conversation
        last_message = (
            db.query(Message)
            .filter(Message.conversation_id == conversation.id)
            .order_by(Message.send_at.desc())
            .first()
        )

        # Extract the last message content and send time
        if last_message:
            last_message_content = last_message.content
            last_message_time = last_message.send_at
        else:
            last_message_content = ""
            last_message_time = None

        # Add conversation data to the list, including the messages
        conversation_data.append({
            "id": conversation.id,
            "current_user_id": current_user.id,
            "name": friend_name,
            "message": last_message_content,
            "messages": messages_data,
            "time": last_message_time,
        })

    return conversation_data

@router.get("/customconversations/{conversation_id}", response_model=dict)
def get_conversation(conversation_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Get the conversation
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Determine the friend's ID based on the conversation
    friend_id = conversation.user2_id if conversation.user1_id == current_user.id else conversation.user1_id

    # Get the friend's name
    friend = db.query(User).filter(User.id == friend_id).first()
    friend_name = f"{friend.firstname} {friend.lastname}"

    # Get all messages in this conversation between the current user and their friend
    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation.id)
        .filter(or_(
            and_(Message.sender_id == current_user.id, Message.receiver_id == friend_id),
            and_(Message.sender_id == friend_id, Message.receiver_id == current_user.id)
        ))
        .order_by(Message.send_at.asc())  # Order by message send time
        .all()
    )

    # Extract the message content and send time
    messages_data = [{
        "content": message.content,
        "time": message.send_at,
        "sender_id": message.sender_id,
    } for message in messages]

    # Get the last message in this conversation
    last_message = (
        db.query(Message)
        .filter(Message.conversation_id == conversation.id)
        .order_by(Message.send_at.desc())
        .first()
    )

    # Extract the last message content and send time
    if last_message:
        last_message_content = last_message.content
        last_message_time = last_message.send_at
    else:
        last_message_content = ""
        last_message_time = None

    # Add conversation data to the list, including the messages
    conversation_data = {
        "id": conversation.id,
        "current_user_id": current_user.id,
        "friend_id": friend_id,
        "name": friend_name,
        "message": last_message_content,
        "messages": messages_data,
        "time": last_message_time,
    }

    return conversation_data


