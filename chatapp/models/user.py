from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column , relationship
from chatapp.models import Model
from chatapp.models.message import Message
from chatapp.models.notification import Notification
from chatapp.models.friendships import Friendship



class User(Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    firstname: Mapped[str] = mapped_column(String(32), nullable=False)
    lastname: Mapped[str] = mapped_column(String(32), nullable=False)
    username: Mapped[str] = mapped_column(String(32), nullable=False, unique=True, index=True)
    email: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    password: Mapped[str] = mapped_column(String(64), nullable=False)
    country: Mapped[str] = mapped_column(String(64))
    city: Mapped[str] = mapped_column(String(64))
    profile_photo_path: Mapped[str] = mapped_column(String(255), nullable=True)

    messages_sent = relationship("Message", foreign_keys=[Message.sender_id], back_populates="sender")
    messages_received = relationship("Message", foreign_keys=[Message.receiver_id], back_populates="receiver")
    sent_notifications = relationship("Notification", foreign_keys=[Notification.sender_id], back_populates="sender")
    received_notifications = relationship("Notification", foreign_keys=[Notification.recipient_id], back_populates="recipient")
     # Define the 'friends' and 'friends_of' relationships
    friends = relationship("Friendship", foreign_keys=[Friendship.user_id], back_populates="user")
    friends_of = relationship("Friendship", foreign_keys=[Friendship.friend_id], back_populates="friend")