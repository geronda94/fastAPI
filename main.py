import time
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
from db import db

app = FastAPI(
    title='Trading app'
)

# uvicorn main:app --reload --host 192.168.205.217 --port 8000

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


fake_users = [
    {'id':1,'role':'admin', 'name':'Bob'},
    {'id':2,'role':'investor', 'name':'Alex'},
    {'id':3,'role':'trader', 'name':'Jhon'},
]


@app.get('/users/{user_id}')
def get_user(user_id: int):
    return [x for x in fake_users if x.get('id') == user_id]


fake_trades = [
    {'id':1, 'user_id':1, 'currency':'BTC', 'side':'buy', 'price':123, 'amount':2.12},
    {'id':2, 'user_id':1, 'currency':'BTC', 'side':'sell', 'price':123, 'amount':2.12}
]


@app.get('/trades')
def get_trades( offset: int, limit: int = 10):
    return fake_trades[offset:][:limit]


fake_users_2 = [
    {'id':1,'role':'admin', 'name':'Bob'},
    {'id':2,'role':'investor', 'name':'Alex'},
    {'id':3,'role':'trader', 'name':'Jhon'},
]


@app.post('/users/{user_id}')
def change_user_name(user_id: int, new_name: str):
    current_user = list(filter(lambda x: x.get('id') == user_id, fake_users_2))[0]
    current_user['name'] = new_name
    return {'status':200, 'data':current_user}

























@app.get('/fake')
async def get_fake():
    res = await db.request('SELECT * FROM test_async_2')
    res2 = await db.request('SELECT * FROM test_async')
    return res,res2








@app.on_event("startup")
async def startup_event():
    await db.connect()
    asyncio.create_task(run_periodically())


# Отключение от базы данных при завершении работы приложения
@app.on_event("shutdown")
async def shutdown_event():
    await db.disconnect()


async def open_and_close_connection():
    await db.disconnect()
    await db.connect()

# Установка асинхронной задачи на выполнение каждые 24 часа
async def run_periodically():
    while True:
        await open_and_close_connection()
        await asyncio.sleep(60*60*24) 
