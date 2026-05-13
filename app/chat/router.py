from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request, Depends, HTTPException, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from typing import List, Dict
from app.chat.dao import MessagesDAO, ChatRoomDAO
from app.chat.schemas import MessageRead, MessageCreate, ChatRoomCreate
from app.users.dependencies import get_current_user
from app.users.models import User
from app.database import async_session_maker
from sqlalchemy import select, and_, or_, delete
from app.chat.models import ChatRoom, ChatMember, Message
import asyncio
import os
import shutil
from datetime import datetime

router = APIRouter(prefix='/chat', tags=['Chat'])
templates = Jinja2Templates(directory='app/templates')

active_connections: Dict[str, WebSocket] = {}

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), room_id: int = None):
    safe_filename = f"{datetime.now().timestamp()}_{file.filename.replace(' ', '_')}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"file_url": f"/uploads/{safe_filename}"}

async def notify_user(user_id: str, message: dict):
    if user_id in active_connections:
        websocket = active_connections[user_id]
        try:
            await websocket.send_json(message)
        except Exception:
            active_connections.pop(user_id, None)

async def notify_room(room_id: int, message: dict, exclude_user_id: str = None):
    from app.chat.models import ChatMember
    async with async_session_maker() as session:
        query = select(ChatMember.user_id).filter(ChatMember.room_id == room_id)
        result = await session.execute(query)
        member_ids = [row[0] for row in result.all()]
        
        for user_id in member_ids:
            if user_id != exclude_user_id:
                await notify_user(user_id, message)

@router.get("/", response_class=HTMLResponse)
async def get_chat_page(request: Request, user_data: User = Depends(get_current_user)):
    return templates.TemplateResponse("chat_groups.html", {
        "request": request, 
        "user": user_data,
        "current_user_tag": user_data.user_tag
    })

@router.get("/chats")
async def get_user_chats(current_user: User = Depends(get_current_user)):
    return await ChatRoomDAO.get_user_chats(current_user.id)

@router.post("/private/create/{user_id}")
async def create_private_chat(user_id: str, current_user: User = Depends(get_current_user)):
    room = await ChatRoomDAO.create_private_chat(current_user.id, [user_id])
    return room

@router.post("/groups/create")
async def create_group_chat(room_data: ChatRoomCreate, current_user: User = Depends(get_current_user)):
    room = await ChatRoomDAO.create_group_chat(
        name=room_data.name,
        created_by_id=current_user.id,
        description=room_data.description
    )
    return room

@router.get("/{room_id}/messages")
async def get_messages(room_id: int, current_user: User = Depends(get_current_user)):
    messages = await MessagesDAO.get_room_messages(room_id)
    return messages

@router.post("/{room_id}/messages")
async def send_message(room_id: int, message: MessageCreate, current_user: User = Depends(get_current_user)):
    message_data = await MessagesDAO.add_message(
        room_id=room_id,
        sender_id=current_user.id,
        content=message.content
    )
    
    await notify_room(room_id, message_data, exclude_user_id=current_user.id)
    
    return message_data

@router.post("/{room_id}/add_member/{user_id}")
async def add_member_to_room(room_id: int, user_id: str, current_user: User = Depends(get_current_user)):
    member = await ChatRoomDAO.add_member(room_id, user_id, current_user.id)
    if not member:
        raise HTTPException(status_code=404, detail="Room not found")
    return {'message': 'User added successfully'}

@router.post("/{room_id}/leave")
async def leave_room(room_id: int, current_user: User = Depends(get_current_user)):
    is_deleted = await ChatRoomDAO.remove_member(room_id, current_user.id)
    return {'message': 'Left room successfully', 'deleted': is_deleted}

@router.get("/{room_id}/info")
async def get_room_info(room_id: int, current_user: User = Depends(get_current_user)):
    async with async_session_maker() as session:
        query = select(ChatRoom).filter(ChatRoom.id == room_id)
        result = await session.execute(query)
        room = result.scalar_one_or_none()
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")
        return {
            'id': room.id,
            'name': room.name if room.name else 'Private Chat',
            'description': room.description,
            'is_private': room.is_private,
            'created_by_id': room.created_by_id
        }

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    active_connections[user_id] = websocket
    try:
        while True:
            await asyncio.sleep(30)
    except (WebSocketDisconnect, asyncio.CancelledError):
        active_connections.pop(user_id, None)

@router.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join("uploads", filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=filename)
    return {"error": "File not found"}

@router.get("/favorites/room")
async def get_favorites_room(current_user: User = Depends(get_current_user)):
    async with async_session_maker() as session:
        query = select(ChatRoom).filter(
            ChatRoom.name == "Избранное",
            ChatRoom.created_by_id == current_user.id
        )
        result = await session.execute(query)
        fav_room = result.scalar_one_or_none()
        
        if fav_room:
            return {"id": fav_room.id, "name": fav_room.name, "exists": True}
        return {"exists": False}
    
@router.get("/{room_id}/members")
async def get_room_members(room_id: int, current_user: User = Depends(get_current_user)):
    async with async_session_maker() as session:
        query = select(User).join(ChatMember).filter(ChatMember.room_id == room_id)
        result = await session.execute(query)
        members = result.scalars().all()
        return [{'id': m.id, 'name': m.name, 'email': m.email, 'user_tag': m.user_tag} for m in members]