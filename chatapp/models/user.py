from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from chatapp.models import Model

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

