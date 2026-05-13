from fastapi import APIRouter, Response, Request, Depends, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List
from sqlalchemy import update, select
from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException, PasswordMismatchException
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dao import UsersDAO
from app.users.schemas import SUserRegister, SUserAuth, SUserRead
from app.users.dependencies import get_current_user
from app.users.models import User
from app.database import async_session_maker
from app.chat.models import ChatRoom, ChatMember, Message  # <-- ДОБАВЛЕНО
import os
import shutil
from datetime import datetime

router = APIRouter(prefix='/auth', tags=['Auth'])
templates = Jinja2Templates(directory='app/templates')

UPLOAD_DIR = "uploads/avatars"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/", response_class=HTMLResponse)
async def get_auth_page(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})

@router.get("/profile", response_class=HTMLResponse)
async def get_profile_page(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("profile.html", {"request": request, "user": current_user})

@router.post("/register/")
async def register_user(user_data: SUserRegister) -> dict:
    user = await UsersDAO.find_one_or_none(email=user_data.email)
    if user:
        raise UserAlreadyExistsException
    
    if user_data.password != user_data.password_check:
        raise PasswordMismatchException("Пароли не совпадают")
    
    hashed_password = get_password_hash(user_data.password)
    
    # Создаём пользователя
    new_user_id = await UsersDAO.add(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_password
    )
    
    # Создаём чат "Избранное" для нового пользователя
    async with async_session_maker() as session:
        async with session.begin():
            fav_room = ChatRoom(
                name="Избранное",
                created_by_id=new_user_id,
                is_private=True
            )
            session.add(fav_room)
            await session.flush()
            
            # Добавляем пользователя в чат
            member = ChatMember(room_id=fav_room.id, user_id=new_user_id, is_admin=True)
            session.add(member)
            await session.flush()
            
            # Приветственное сообщение
            welcome_message = f"Здравствуйте, {user_data.name}!\n\nДобро пожаловать в мессенджер Вейрикс (Weyrix)! Мессенджер находится в разработке, а пока вы можете протестировать его и попробовать пообщаться с другими пользователями, которые есть в системе. Используйте строку поиска для того, чтобы найти своего собеседника, вписав id пользователя в строку поиска. В настройках ты можешь поменять тему мессенджера или язык. Проект находится на стадии развития и в ближайшем будущем планируется активное обновление мессенджера. Спасибо за тестирование мессенджера Weyrix!"            

            message = Message(
                room_id=fav_room.id,
                sender_id=new_user_id,
                content=welcome_message,
                is_system=True
            )
            session.add(message)
            await session.commit()
    
    return {'message': 'Вы успешно зарегистрированы!'}

@router.post("/login/")
async def auth_user(response: Response, user_data: SUserAuth):
    check = await authenticate_user(email=user_data.email, password=user_data.password)
    if check is None:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'ok': True, 'access_token': access_token, 'message': 'Авторизация успешна!'}

@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}

@router.get("/users", response_model=List[SUserRead])
async def get_users():
    users_all = await UsersDAO.find_all()
    return [{'id': user.id, 'name': user.name} for user in users_all]

@router.get("/search/{user_tag}")
async def search_user(user_tag: str):
    async with async_session_maker() as session:
        query = select(User).filter(User.user_tag == user_tag)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        if user:
            return {'id': user.id, 'user_tag': user.user_tag, 'name': user.name, 'email': user.email}
        return None

@router.post("/update_name")
async def update_name(name_data: dict, current_user: User = Depends(get_current_user)):
    async with async_session_maker() as session:
        async with session.begin():
            query = update(User).where(User.id == current_user.id).values(name=name_data['name'])
            await session.execute(query)
            await session.commit()
    return {'message': 'Name updated'}

@router.post("/update_email")
async def update_email(email_data: dict, current_user: User = Depends(get_current_user)):
    async with async_session_maker() as session:
        async with session.begin():
            query = update(User).where(User.id == current_user.id).values(email=email_data['email'])
            await session.execute(query)
            await session.commit()
    return {'message': 'Email updated'}

@router.post("/upload_avatar")
async def upload_avatar(avatar: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    file_ext = os.path.splitext(avatar.filename)[1]
    filename = f"{current_user.id}_{int(datetime.now().timestamp())}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(avatar.file, buffer)
    
    async with async_session_maker() as session:
        async with session.begin():
            query = update(User).where(User.id == current_user.id).values(avatar=filename)
            await session.execute(query)
            await session.commit()
    
    return {"avatar_url": f"/uploads/avatars/{filename}"}

@router.get("/user/{user_id}")
async def get_user_info(user_id: int, current_user: User = Depends(get_current_user)):
    user = await UsersDAO.find_one_or_none_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'avatar': user.avatar
    }

@router.get("/user/{user_id}/profile", response_class=HTMLResponse)
async def get_user_profile_page(request: Request, user_id: int, current_user: User = Depends(get_current_user)):
    user = await UsersDAO.find_one_or_none_by_id(user_id)
    if not user:
        return HTMLResponse(content="User not found", status_code=404)
    return templates.TemplateResponse("user_profile.html", {"request": request, "profile_user": user, "current_user": current_user})