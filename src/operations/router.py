import datetime
from typing import List, Type
from pydantic import BaseModel
from sqlalchemy import insert, select
from fastapi import APIRouter, Depends, HTTPException
from database import AsyncSession, get_async_session
from operations.models import operation
from operations.schemas import OperationCreate, OperationModel
from typing import Annotated
from fastapi_cache.decorator import cache 




router = APIRouter(
    prefix='/operations',
    tags=['Operation']
)


class ResponseModel(BaseModel):
    status: str = 'success'
    data: Annotated[List[OperationModel] , None] = None
    details: str | None = None


@router.get('/{operation_type}', response_model=ResponseModel)
@cache(expire=60*30)##значение expire в секундах
async def get_specific_operations(operation_type: str | None = None, session: AsyncSession = Depends(get_async_session)):
    try:
        operation_type = 'sell' if operation_type is None else operation_type

        query = select(operation).where(operation.c.type == operation_type)
        result = await session.execute(query)       
        res = result.mappings().all()
        return {'data':res}
        

    except Exception as ex:
        raise HTTPException(
            status_code=500,
            detail=str(ex)
        )
        
        
        
@router.post('/')
async def add_specific_operation(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(operation).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
        
    return {'status':'ok'}