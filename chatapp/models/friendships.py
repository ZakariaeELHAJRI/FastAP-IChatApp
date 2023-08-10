from chatapp.models import Model
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String , ForeignKey
from sqlalchemy.orm import relationship


class Friendship(Model):
    __tablename__ = "friendship"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id: Mapped[int] = mapped_column(Integer,ForeignKey('user.id'), nullable=False )
    friend_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id') , nullable=False)
    status: Mapped[str] = mapped_column(String(64), nullable=False) # pending, accepted, rejected

    user = relationship("User", foreign_keys=[user_id], back_populates="friends")
    friend = relationship("User", foreign_keys=[friend_id], back_populates="friends_of")
    