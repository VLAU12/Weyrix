import os
from sqlalchemy import func
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession

# Берём URL базы данных из переменной окружения Render
# Если переменной нет — используем SQLite (для локальной разработки)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///db.sqlite3")

# Для PostgreSQL добавляем asyncpg драйвер
if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())