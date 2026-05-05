from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List, Dict
from app.chat.dao import MessagesDAO, DialogsDAO
from app.chat.schemas import MessageRead, MessageCreate
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.users.models import User
import asyncio

router = APIRouter(prefix='/chat', tags=['Chat'])
templates = Jinja2Templates(directory='app/templates')

active_connections: Dict[int, WebSocket] = {}

async def notify_user(user_id: int, message: dict):
    if user_id in active_connections:
        websocket = active_connections[user_id]
        await websocket.send_json(message)

@router.get("/", response_class=HTMLResponse)
async def get_chat_page(request: Request, user_data: User = Depends(get_current_user)):
    dialogs = await DialogsDAO.get_user_dialogs(user_data.id)
    return templates.TemplateResponse("chat.html", {
        "request": request, 
        "user": user_data, 
        "dialogs": dialogs
    })

@router.get("/dialog/{user_id}", response_model=List[MessageRead])
async def get_dialog_messages(user_id: int, current_user: User = Depends(get_current_user)):
    return await MessagesDAO.get_messages_between_users(user_id_1=user_id, user_id_2=current_user.id) or []

@router.post("/messages")
async def send_message(message: MessageCreate, current_user: User = Depends(get_current_user)):
    message_data = await MessagesDAO.add_message_to_dialog(
        sender_id=current_user.id,
        recipient_id=message.recipient_id,
        content=message.content
    )
    
    # created_at уже строка из dao.py, не нужно преобразовывать
    
    await notify_user(message.recipient_id, message_data)
    await notify_user(current_user.id, message_data)
    
    return {'status': 'ok', 'message': 'Message saved!'}

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    active_connections[user_id] = websocket
    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        active_connections.pop(user_id, None)