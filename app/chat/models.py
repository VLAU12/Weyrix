from sqlalchemy import Integer, Text, ForeignKey, DateTime, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.database import Base
from sqlalchemy import Integer, Text, ForeignKey, DateTime, Boolean
from datetime import datetime


class ChatRoom(Base):
    __tablename__ = 'chat_rooms'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=True)  # Для приватных чатов может быть null
    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_by_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    is_private: Mapped[bool] = mapped_column(Boolean, default=True)  # По умолчанию приватный
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)  # Для удаления чата


class ChatMember(Base):
    __tablename__ = 'chat_members'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    room_id: Mapped[int] = mapped_column(Integer, ForeignKey("chat_rooms.id"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_read_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)


class Message(Base):
    __tablename__ = 'messages'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    room_id: Mapped[int] = mapped_column(Integer, ForeignKey("chat_rooms.id"))
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    is_system: Mapped[bool] = mapped_column(Boolean, default=False)
    is_favorite: Mapped[bool] = mapped_column(Boolean, default=False)