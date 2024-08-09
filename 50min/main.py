from typing import Annotated
from fastapi import Depends, FastAPI
from pydantic import BaseModel


app = FastAPI()




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