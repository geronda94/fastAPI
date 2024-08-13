from typing import Annotated
from fastapi import Depends, FastAPI
from pydantic import BaseModel

from contextlib import asynccontextmanager
from database import create_tables, drop_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await drop_tables()
    print('База очищена')
    await create_tables()
    print('База готова')
    yield 
    print ('Перезагрузка')



app = FastAPI(lifespan=lifespan)




class StaskAdd(BaseModel):
    name: str
    description: str | None


class STask(BaseModel):
    id: int

tasks = []

# @app.get('/tasks')
# def get_tasks():
     
#      return {'data':task}

@app.post("/tasks")
async def add_task(
    task: Annotated[StaskAdd, Depends()]
):
    tasks.append(task)
    return {'ok': True}