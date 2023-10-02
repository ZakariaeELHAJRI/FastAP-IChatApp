from sqlalchemy.orm import Session
# import user model
from chatapp.models.conversation import Conversation

def create_conversation(db: Session, conversation_data: dict):
    # Check if a conversation already exists between user1 and user2
    existing_conversation = db.query(Conversation).filter(
        ((Conversation.user1_id == conversation_data['user1_id']) & (Conversation.user2_id == conversation_data['user2_id'])) |
        ((Conversation.user1_id == conversation_data['user2_id']) & (Conversation.user2_id == conversation_data['user1_id']))
    ).first()

    if existing_conversation:
        # Conversation already exists, return it or handle the duplication as needed
        return existing_conversation

    # If no existing conversation found, create a new one
    conversation = Conversation(**conversation_data)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation

def get_conversation(db: Session, conversation_id: int):
    return db.query(Conversation).filter(Conversation.id == conversation_id).first()

def get_conversations(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Conversation).offset(skip).limit(limit).all()

def update_conversation(db: Session, conversation_id: int, conversation_data: dict):
    conversation = get_conversation(db, conversation_id)
    if conversation is None:
        return None
    for key, value in conversation_data.items():
        setattr(conversation, key, value)
    db.commit()
    db.refresh(conversation)
    return conversation

def delete_conversation(db: Session, conversation_id: int):
    conversation = get_conversation(db, conversation_id)
    if conversation is None:
        return False
    db.delete(conversation)
    db.commit()
    return True

