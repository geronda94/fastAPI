import datetime
from typing import List, Type
from pydantic import BaseModel
from sqlalchemy import insert, select
from fastapi import APIRouter, Depends
from database import AsyncSession, get_async_session
from operations.models import operation
from operations.schemas import OperationCreate, OperationModel


router = APIRouter(
    prefix='/operations',
    tags=['Operation']
)




@router.get('/}', response_model=List[OperationModel])
async def get_specific_operation(operation_type:None, session: AsyncSession = Depends(get_async_session)):
    query = select(operation).where(operation.c.type == 'sell')
    result = await session.execute(query)
    res = result.all()
    return res
        
        
@router.post('/')
async def add_specific_operation(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(operation).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
        
    return {'status':'ok'}