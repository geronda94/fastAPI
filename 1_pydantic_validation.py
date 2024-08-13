import datetime
from typing import List, Optional
from fastapi import FastAPI, Request, status # type: ignore
from pydantic import BaseModel, Field #type: ignore
from enum import Enum





app = FastAPI(
    title='Trading app'
)

class DegreeType(Enum):
    newbie = 'newbie'
    expert= 'expert'


class Degree(BaseModel):
    id: int
    created_at: datetime.datetime
    type_degree: DegreeType


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] = []


fake_trades = [
    {'id':1, 'role':'admin', 'name': 'Bob'},
    {'id':2, 'role':'investor', 'name': 'Goga'},
    {'id':3, 'role':'trader', 'name': 'Bill'},
    {'id':4, 'role':'investor', 'name': 'Homer', 
     'degree':[{
            'id':1, 'created_at': '2020-01-01T00:00:00', 'type_degree':'expert'
     }]
    },
]


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=5)
    side: str
    price: float = Field(ge=0)
    amount: float




@app.get('/users/{user_id}', response_model=List[User])
def get_user(user_id: int):
    return [user for user in fake_trades if user['id']== int(user_id)]


@app.post('/trades')
def add_trades(trades: List[Trade]):
    fake_trades.extend(trades)
    return {'status': 200, 'data': fake_trades}