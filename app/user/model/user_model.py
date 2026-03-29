from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from app.db import Base



class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=True)
    email = Column(String(255), unique=True, nullable=True)
    password = Column(String(255), nullable=False)
    
    items = relationship("Item", back_populates="user")  # attribute .user in class Item