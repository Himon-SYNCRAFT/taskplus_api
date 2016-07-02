from database import Model
from sqlalchemy import Column, Integer, String


class User(Model):
    __tablename__ = 'user'

    id = Column(Integer(), primary_key=True)
    name = Column(String(length=128), unique=True, nullable=False)
