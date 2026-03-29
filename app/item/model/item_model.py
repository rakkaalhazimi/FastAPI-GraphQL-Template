from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.db import Base



class Item(Base):
    __tablename__ = "item"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(Text)
    user_id = Column(ForeignKey("user.id"))  # column 'id' in user table
    user = relationship("User", back_populates="items")  # attribute .items in User class