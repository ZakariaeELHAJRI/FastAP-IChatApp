from chatapp.models import Model

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String , ForeignKey , DateTime , func
from datetime import datetime
from sqlalchemy.orm import relationship


class Message(Model):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    sender_id: Mapped[int] = mapped_column(Integer,ForeignKey('user.id'), nullable=False )
    receiver_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id') , nullable=False)
    content: Mapped[str] = mapped_column(String(256), nullable=False)
    send_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())

    sender = relationship("User", foreign_keys=[sender_id], back_populates="messages_sent")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="messages_received")
    
