from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class MessageRead(BaseModel):
    id: int
    room_id: int
    sender_id: int
    content: str
    created_at: Optional[datetime] = None
    is_system: bool = False

class MessageCreate(BaseModel):
    content: str

class ChatRoomCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None

class ChatRoomRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_by_id: int
    created_at: datetime
    is_private: bool