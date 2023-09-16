from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import UniqueConstraint
from chatapp.models import Model
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Conversation(Model):
    __tablename__ = "conversation"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user1_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    user2_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    
    # Define a composite unique constraint to ensure uniqueness of conversations
    __table_args__ = (
        UniqueConstraint('user1_id', 'user2_id', name='_user_user_uc'),
    )
    
    # Relationship to link this Conversation model to the users
    user1 = relationship("User", foreign_keys=[user1_id])
    user2 = relationship("User", foreign_keys=[user2_id])

    messages = relationship("Message", back_populates="conversation")

    def __init__(self, user1_id: int, user2_id: int):
        self.user1_id = user1_id
        self.user2_id = user2_id

    def __str__(self):
        return f"Conversation between User {self.user1_id} and User {self.user2_id}"
