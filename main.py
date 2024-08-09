from datetime import datetime
from enum import Enum
import time
from typing import List, Optional, Union
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import asyncio
from db import db




app = FastAPI(
    title='Trading app'
)

# uvicorn main:app --reload --host 192.168.205.217 --port 8000


@app.exception_handler(ValidationException)
async def validation_except_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({'detail':exc.errors()}),
    )





class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


fake_users = [
    {'id':1,'role':'admin', 'name':['Bob']},
    {'id':2,'role':'investor', 'name':'Alex'},
    {'id':3,'role':'trader', 'name':'Jhon'},
    {'id':4,'role':'investor', 'name':'Homer', 'degree':[
            {'id':1, 'created_at':'2020-01-01T00:00:00', 'type_degree':'newbie'}
        ]
    }
]



class DegreeType(Enum):
    newbie ='newbie'
    expert ='expert'


class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] =[]


@app.get('/users/{user_id}', response_model=List[User])
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





class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=5)
    side: str
    price: float = Field(ge=0)
    amount: float


@app.post('/trades')
def add_trades(trades: list[Trade]):
    fake_trades.extend(trades)
    return {'status':200, 'data':fake_trades}





















@app.get('/fake')
async def get_fake():
    res = await db.request('SELECT * FROM test_async_2')
    res2 = await db.request('SELECT * FROM test_async')
    return res,res2








# Обработчик события "startup"
async def startup_event():
    await db.connect()
    asyncio.create_task(run_periodically())

# Обработчик события "shutdown"
async def shutdown_event():
    await db.disconnect()

# Регистрация обработчиков событий жизненного цикла с помощью LifespanManager
app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)

async def open_and_close_connection():
    await db.disconnect()
    await db.connect()

# Установка асинхронной задачи на выполнение каждые 24 часа
async def run_periodically():
    while True:
        await open_and_close_connection()
        await asyncio.sleep(60*60*24) 
