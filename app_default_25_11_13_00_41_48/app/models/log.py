from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, func
from app.database import Base


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String(64), unique=True, nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    level = Column(String(20), nullable=False)
    source = Column(String(50), nullable=False)  # e.g., 'backend' or 'bot'
    message = Column(String, nullable=False)
    context = Column(JSON, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
