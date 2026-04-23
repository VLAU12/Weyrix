from sqlalchemy import func
from datetime import datetime
from sqlalchemy.orm import Maped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAtters, async_sessionmaker, create_async_engine, AsyncSession

database_url = 'sqlite+aiosqlite:///db.sqlite3'
engine = create_async_engine(url=database_url)
async_session_makerb = async_sessionmaker(engine, class_=AsyncSession)

class Base(AsyncAtters, DeclarativeBase):
    created_at: Maped[datetime] = mapped_column(server_default=func.now())
    updeted_at: Maped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

