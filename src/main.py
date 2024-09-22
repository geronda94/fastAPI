import json
from typing import Any
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from pydantic import BaseModel
from database import redis

from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserCreate, UserRead
from operations.router import router as router_operation
from tasks.router import router as router_tasks
from pages.router import router as router_pages
from chat.router import router as router_chat
from auth.router import router as router_auth

from contextlib import asynccontextmanager



app = FastAPI(
    title="Trading App"
)



async def get_async_session():
    print('Получение сессии')
    session = 'session'
    yield 0
    print(' сессии')
    
    
    

def pagination_params(limit:int =10, skip:int = 0):
    return {"limit":limit, 'skip':skip}


pagination = Depends(pagination_params)

class Paginator:
    def __init__(self, limit:int =10, skip:int = 0):
        self.limit = limit
        self.skip = skip

pg_class = Paginator(2,3)


@app.get('/subject-class')
def get_subject(pagination_params: Paginator = Depends()):
    return pagination_params



@app.get('/subject')
def get_subject(pagination_params: dict = pagination):
    return pagination_params


class AuthGuard:
    def __init__(self, app: str):
        self.app = app
        
    def __call__(self, request: Request) -> Any:
        if 'bonds' not in request.cookies:
            raise HTTPException(status_code=403, detail='Запрещено!')
        
        return True 
     
auth_guard_payments = AuthGuard('payments')

@app.get('/get_payments', dependencies=[Depends(auth_guard_payments)])
async def get_payments(request: Request, auth_guard_payments: AuthGuard = Depends(auth_guard_payments)):
    return request.client






app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)


app.include_router(router_operation)
app.include_router(router_auth)
app.include_router(router_tasks)
app.include_router(router_pages)
app.include_router(router_chat)


origins = [
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

@app.on_event("startup")
async def startup_event():
    
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    
    
@app.get('/items')
async def get_items(session=Depends(get_async_session)):
    return [{"id":session}]