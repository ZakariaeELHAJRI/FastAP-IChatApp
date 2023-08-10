from sqlalchemy.orm import DeclarativeBase

# models
class Model(DeclarativeBase):
    pass

# imports
from chatapp.models.user import User
from chatapp.models.message import Message
