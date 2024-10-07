import json
from typing import Any
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from pydantic import BaseModel
from sqlalchemy import select
from database import redis, AsyncSession, get_async_session

from auth.base_config import auth_backend, fastapi_users, current_user
from auth.schemas import UserCreate, UserRead
# from operations.router import router as router_operation
from orders.models import Site
# from tasks.router import router as router_tasks
from auth.router import router as router_auth
from auth.roles import role, permission, Perms
from auth.models import User, Roles
from orders.router import router as router_orders

from apscheduler.schedulers.asyncio import AsyncIOScheduler


app = FastAPI(
    title="Multi Page Service",
    openapi_prefix="/api"
)
scheduler = AsyncIOScheduler()



    


    

def pagination_params(limit:int =10, skip:int = 0):
    return {"limit":limit, 'skip':skip}


pagination = Depends(pagination_params)

class Paginator:
    def __init__(self, limit:int =10, skip:int = 0):
        self.limit = limit
        self.skip = skip

pg_class = Paginator(2,3)


@app.get('/subject-class')
@role([Roles.admin])
async def get_subject(user: User = Depends(current_user),
                pagination_params: Paginator = Depends()
                ):
    return pagination_params



@app.get('/subject')
@permission([Perms.READ])
async def get_subject(user: User = Depends(current_user),
                      pagination_params: dict = pagination):
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
@role([Roles.admin])
async def get_payments(request: Request, 
                       auth_guard_payments: AuthGuard = Depends(auth_guard_payments),
                       user: User = Depends(current_user)
                       ):
    return request.client






app.mount("/static", StaticFiles(directory="static"), name="static")


# app.include_router(router_operation)
app.include_router(router_orders)
app.include_router(router_auth)
# app.include_router(router_tasks)
# app.include_router(router_pages)
# app.include_router(router_chat)
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










origins = [    
    "http://localhost",
    "https://localhost"
    "http://localhost:8000",
    "https://localhost:8000",
    "https://it-igor.click"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", 
                   "Access-Control-Allow-Origin", "Authorization"],
)

cached_sites = {}

async def cache_sites(session: AsyncSession):
    result = await session.execute(select(Site))  # Предполагаем, что у вас есть модель Site
    sites = result.scalars().all()
    return {site.site_name: site for site in sites}  # Возвращаем кэш как словарь

async def update_cache():
    async for session in get_async_session():  # Получаем сессию
        global cached_sites
        cached_sites = await cache_sites(session)  # Обновляем кэш
        break  # Прерываем цикл после получения первой сессии

async def update_origins():
    global origins
    await update_cache()  # Обновляем кэш

    # Обновляем список origins на основе кэшированных сайтов
    new_origins = [f"{protocol}://{site.site_name}" for site in cached_sites.values() for protocol in ["http", "https"]]

    for new_origin in new_origins:
        if new_origin not in origins:
            origins.append(new_origin)


@app.on_event("startup")
async def startup_event():
    await update_origins()  # Обновляем origins при запуске
    scheduler.add_job(update_origins, 'interval', minutes=2) 
    scheduler.start()

@app.get('/origins')
async def get_origins():
    return origins  # Возвращаем текущий список origins