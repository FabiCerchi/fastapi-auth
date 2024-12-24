from app.db.db import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.schema import ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    last_name = Column(String, index=True)
    age = Column(Integer)
    address = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    state = Column(Boolean, default=False)
    sale_id = relationship("Sale", backref="user", cascade="delete,merge") # Referencia uno a muchos


class Sale(Base):
    __tablename__ = "sale"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), index=True) # Relación uno a muchos
    product = Column(String, index=True)
    price = Column(Integer)
    created_at = Column(DateTime, default=datetime.now())
    state = Column(Boolean)