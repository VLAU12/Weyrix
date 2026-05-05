from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class MessageRead(BaseModel):
    id: int
    sender_id: int
    recipient_id: int
    content: str
    created_at: Optional[datetime] = None

class MessageCreate(BaseModel):
    recipient_id: int
    content: str

class DialogRead(BaseModel):
    dialog_id: int
    user_id: int
    user_name: str
    last_message: Optional[str] = ""
    last_message_time: Optional[datetime] = None