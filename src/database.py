from typing import AsyncGenerator

from redis import asyncio as aioredis
from sqlalchemy import MetaData, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
Base = declarative_base()


engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
        
        
        






#Примеры работы с асинхронной сессией
async def check_orders():
    async for session in get_async_session():  # Получаем сессию из генератора
        # Работаем с сессией (можно сразу использовать ее)
        result = await session.execute(text("SELECT * FROM orders"))
        orders = result.mappings().all()




async def check_orders1():
    session_generator = get_async_session()
    session = await anext(session_generator)
    try:
        # Работаем с сессией
        result = await session.execute(text("SELECT * FROM orders"))
        orders = result.mappings().all()  # Извлекаем все заказы
    finally:
        await session.close()
