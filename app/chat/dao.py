from sqlalchemy import select, and_, or_, desc
from app.dao.base import BaseDAO
from app.chat.models import Message, Dialog
from app.database import async_session_maker
from datetime import datetime

class MessagesDAO(BaseDAO):
    model = Message
    
    @classmethod
    async def get_messages_between_users(cls, user_id_1: int, user_id_2: int):
        async with async_session_maker() as session:
            query = select(Dialog).filter(
                or_(
                    and_(Dialog.user1_id == user_id_1, Dialog.user2_id == user_id_2),
                    and_(Dialog.user1_id == user_id_2, Dialog.user2_id == user_id_1)
                )
            )
            result = await session.execute(query)
            dialog = result.scalar_one_or_none()
            
            if not dialog:
                return []
            
            query = select(Message).filter(Message.dialog_id == dialog.id).order_by(Message.id)
            result = await session.execute(query)
            return list(result.scalars().all())
    
    @classmethod
    async def add_message_to_dialog(cls, sender_id: int, recipient_id: int, content: str):
        async with async_session_maker() as session:
            async with session.begin():
                query = select(Dialog).filter(
                    or_(
                        and_(Dialog.user1_id == sender_id, Dialog.user2_id == recipient_id),
                        and_(Dialog.user1_id == recipient_id, Dialog.user2_id == sender_id)
                    )
                )
                result = await session.execute(query)
                dialog = result.scalar_one_or_none()
                
                if not dialog:
                    dialog = Dialog(
                        user1_id=sender_id, 
                        user2_id=recipient_id
                    )
                    session.add(dialog)
                    await session.flush()
                
                message = Message(
                    dialog_id=dialog.id,
                    sender_id=sender_id,
                    recipient_id=recipient_id,
                    content=content
                )
                session.add(message)
                
                dialog.last_message = content[:100]
                dialog.last_message_time = datetime.utcnow()
                
                await session.flush()
                
                message_id = message.id
                created_at = datetime.utcnow()
            
            return {
                'id': message_id,
                'sender_id': sender_id,
                'recipient_id': recipient_id,
                'content': content,
                'created_at': created_at.isoformat()
            }


class DialogsDAO(BaseDAO):
    model = Dialog
    
    @classmethod
    async def get_user_dialogs(cls, user_id: int):
        async with async_session_maker() as session:
            from app.users.models import User
            
            query = select(Dialog).filter(
                or_(Dialog.user1_id == user_id, Dialog.user2_id == user_id)
            ).order_by(desc(Dialog.last_message_time))
            result = await session.execute(query)
            dialogs = result.scalars().all()
            
            result_list = []
            for dialog in dialogs:
                other_user_id = dialog.user2_id if dialog.user1_id == user_id else dialog.user1_id
                
                user_query = select(User.name).filter(User.id == other_user_id)
                user_result = await session.execute(user_query)
                other_user_name = user_result.scalar()  # <-- ИСПРАВЛЕНО: была пропущена эта строка
                
                result_list.append({
                    'dialog_id': dialog.id,
                    'user_id': other_user_id,
                    'user_name': other_user_name or 'Unknown',
                    'last_message': dialog.last_message or '',
                    'last_message_time': dialog.last_message_time
                })
            return result_list