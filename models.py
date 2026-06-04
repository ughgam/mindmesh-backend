from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    articles = relationship("Article", back_populates="owner")

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    url = Column(String, nullable=False)
    title = Column(String, nullable=True)
    extracted_text = Column(Text, nullable=True)
    categories = Column(String, nullable=True) 
    metadata_info = Column(JSON, nullable=True) 
    created_at = Column(DateTime, default=datetime.utcnow)
    owner = relationship("User", back_populates="articles")
