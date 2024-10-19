import json

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from typing import Any
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import httpx
from pydantic import BaseModel
from sqlalchemy import select
from database import redis, AsyncSession, get_async_session

from auth.base_config import auth_backend, fastapi_users, current_user
from auth.schemas import UserCreate, UserRead
# from operations.router import router as router_operation

# from tasks.router import router as router_tasks
from auth.router import router as router_auth
from auth.roles import role, permission, Perms
from auth.models import User, Roles


from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import CAPTCHA_SECRET


app = FastAPI(
    title="Multi Page Service",
    openapi_prefix="/api"
)
scheduler = AsyncIOScheduler()






# @app.post("/verify-recaptcha")
# async def verify_recaptcha(token: str):
#     payload = {
#         'secret': CAPTCHA_SECRET,
#         'response': token
#     }
    
#     async with httpx.AsyncClient() as client:
#         response = await client.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
#         result = response.json()
    
#     if result.get("success"):
#         score = result.get("score", 0)
#         return {"score": score}
#     else:
#         raise HTTPException(status_code=400, detail="reCAPTCHA verification failed")
    


    






# @app.get("/admin-panel")
# @role([Roles.admin.value])
# async def admin_panel():
#     return {"message": "Welcome to the admin panel"}





app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router_auth)

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
    "https://localhost",
    "http://localhost:5173",
    "https://localhost:5173",
    "http://localhost:8000",
    "https://localhost:8000",
    "null",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", 
                   "Access-Control-Allow-Origin", "Authorization"],
)




@app.on_event("startup")
async def startup_event():
    scheduler.start()

