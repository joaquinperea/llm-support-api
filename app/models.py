from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Text, func

Base = declarative_base()

class ChatHistory(Base):
    """Model for storing chat history."""
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    model = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
