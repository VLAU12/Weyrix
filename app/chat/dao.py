from sqlalchemy import select, and_, or_, desc, func, delete
from app.dao.base import BaseDAO
from app.chat.models import ChatRoom, ChatMember, Message
from app.database import async_session_maker
from datetime import datetime

class ChatRoomDAO(BaseDAO):
    model = ChatRoom
    
    @classmethod
    async def create_private_chat(cls, created_by_id: str, member_ids: list = None):
        async with async_session_maker() as session:
            async with session.begin():
                if member_ids and len(member_ids) == 1:
                    user1_id = created_by_id
                    user2_id = member_ids[0]
                    
                    room_query = select(ChatRoom).filter(
                        and_(
                            ChatRoom.is_private == True,
                            ChatRoom.name == None
                        )
                    ).join(ChatMember).filter(
                        ChatMember.user_id.in_([user1_id, user2_id])
                    ).group_by(ChatRoom.id).having(
                        func.count(ChatMember.user_id) == 2
                    )
                    result = await session.execute(room_query)
                    existing_room = result.scalar_one_or_none()
                    
                    if existing_room:
                        return existing_room
                
                room = ChatRoom(
                    created_by_id=created_by_id,
                    is_private=True,
                    name=None
                )
                session.add(room)
                await session.flush()
                
                creator_member = ChatMember(room_id=room.id, user_id=created_by_id, is_admin=True)
                session.add(creator_member)
                
                if member_ids:
                    for user_id in member_ids:
                        if user_id != created_by_id:
                            member = ChatMember(room_id=room.id, user_id=user_id)
                            session.add(member)
                
                await session.commit()
                return room
    
    @classmethod
    async def create_group_chat(cls, name: str, created_by_id: str, description: str = None):
        async with async_session_maker() as session:
            async with session.begin():
                room = ChatRoom(
                    name=name,
                    description=description,
                    created_by_id=created_by_id,
                    is_private=False
                )
                session.add(room)
                await session.flush()
                
                member = ChatMember(room_id=room.id, user_id=created_by_id, is_admin=True)
                session.add(member)
                
                await session.commit()
                return room
    
    @classmethod
    async def get_user_chats(cls, user_id: str):
        async with async_session_maker() as session:
            query = select(ChatRoom).join(ChatMember).filter(
                and_(
                    ChatMember.user_id == user_id,
                    ChatRoom.is_active == True
                )
            ).order_by(ChatRoom.created_at.desc())
            result = await session.execute(query)
            rooms = result.scalars().all()
            
            result_list = []
            for room in rooms:
                room_name = room.name
                
                if room.is_private and not room.name:
                    other_member_query = select(ChatMember).filter(
                        and_(ChatMember.room_id == room.id, ChatMember.user_id != user_id)
                    )
                    other_result = await session.execute(other_member_query)
                    other_member = other_result.scalar_one_or_none()
                    
                    if other_member:
                        from app.users.models import User
                        user_query = select(User.name).filter(User.id == other_member.user_id)
                        user_result = await session.execute(user_query)
                        other_user_name = user_result.scalar()
                        if other_user_name:
                            room_name = other_user_name
                
                last_msg_query = select(Message).filter(Message.room_id == room.id).order_by(Message.id.desc()).limit(1)
                last_msg_result = await session.execute(last_msg_query)
                last_message = last_msg_result.scalar_one_or_none()
                
                result_list.append({
                    'id': room.id,
                    'name': room_name or f'Chat_{room.id}',
                    'description': room.description,
                    'is_private': room.is_private,
                    'last_message': last_message.content[:50] if last_message else '',
                    'last_message_time': last_message.created_at if last_message else None,
                })
            return result_list
    
    @classmethod
    async def add_member(cls, room_id: int, user_id: str, current_user_id: str = None):
        async with async_session_maker() as session:
            async with session.begin():
                room_query = select(ChatRoom).filter(and_(ChatRoom.id == room_id, ChatRoom.is_active == True))
                room_result = await session.execute(room_query)
                room = room_result.scalar_one_or_none()
                
                if not room:
                    return None
                
                query = select(ChatMember).filter(
                    and_(ChatMember.room_id == room_id, ChatMember.user_id == user_id)
                )
                result = await session.execute(query)
                existing = result.scalar_one_or_none()
                
                if existing:
                    return existing
                
                member = ChatMember(room_id=room_id, user_id=user_id)
                session.add(member)
                
                from app.users.models import User
                user_query = select(User.name).filter(User.id == user_id)
                user_result = await session.execute(user_query)
                user_name = user_result.scalar()
                
                system_msg = Message(
                    room_id=room_id,
                    sender_id=user_id,
                    content=f"👤 Пользователь {user_name} присоединился к чату",
                    is_system=True
                )
                session.add(system_msg)
                
                await session.commit()
                return member
    
    @classmethod
    async def remove_member(cls, room_id: int, user_id: str):
        async with async_session_maker() as session:
            async with session.begin():
                query = delete(ChatMember).where(
                    and_(ChatMember.room_id == room_id, ChatMember.user_id == user_id)
                )
                await session.execute(query)
                
                members_query = select(ChatMember).filter(ChatMember.room_id == room_id)
                members_result = await session.execute(members_query)
                remaining_members = members_result.scalars().all()
                
                if not remaining_members:
                    await session.execute(
                        delete(ChatRoom).where(ChatRoom.id == room_id)
                    )
                    return True
                
                from app.users.models import User
                user_query = select(User.name).filter(User.id == user_id)
                user_result = await session.execute(user_query)
                user_name = user_result.scalar()
                
                system_msg = Message(
                    room_id=room_id,
                    sender_id=user_id,
                    content=f"👋 Пользователь {user_name} покинул чат",
                    is_system=True
                )
                session.add(system_msg)
                
                await session.commit()
                return False


class MessagesDAO(BaseDAO):
    model = Message
    
    @classmethod
    async def get_room_messages(cls, room_id: int, limit: int = 100, offset: int = 0):
        async with async_session_maker() as session:
            query = select(Message).filter(
                Message.room_id == room_id
            ).order_by(Message.id).limit(limit).offset(offset)
            result = await session.execute(query)
            return list(result.scalars().all())
    
    @classmethod
    async def add_message(cls, room_id: int, sender_id: str, content: str, is_system: bool = False):
        async with async_session_maker() as session:
            async with session.begin():
                message = Message(
                    room_id=room_id,
                    sender_id=sender_id,
                    content=content,
                    is_system=is_system
                )
                session.add(message)
                await session.flush()
                
                return {
                    'id': message.id,
                    'room_id': room_id,
                    'sender_id': sender_id,
                    'content': content,
                    'created_at': datetime.utcnow().isoformat(),
                    'is_system': is_system
                }