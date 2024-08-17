import datetime
from typing import List, Optional, Union
from fastapi import FastAPI, Request, status, Depends # type: ignore
from pydantic import BaseModel, Field #type: ignore
from enum import Enum
from fastapi_users import FastAPIUsers
from auth.auth import auth_backend
from auth.manager import get_user_manager
from auth.schemas import UserCreate, UserRead
from auth.database import User



app = FastAPI(
    title='Trading app'
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend]
)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth']
)

current_user = fastapi_users.current_user()

@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"

@app.get("/unprotected-route")
def protected_route():
    return f"Hello, annonym"