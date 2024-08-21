import datetime
from typing import List, Type
from pydantic import BaseModel
from sqlalchemy import insert, select
from fastapi import APIRouter, Depends, HTTPException
from database import AsyncSession, get_async_session
from operations.models import operation
from operations.schemas import OperationCreate, OperationModel
from typing import Optional, Any

router = APIRouter(
    prefix='/operations',
    tags=['Operation']
)


class ResponseModel(BaseModel):
    status: str
    data: Optional[List[OperationModel]] = None
    details: Optional[str] = None


@router.get('/}', response_model=ResponseModel)
async def get_specific_operation(operation_type, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(operation).where(operation.c.type == 'sell')
        result = await session.execute(query)
        res = result.mappings().all()
        return ResponseModel(
            status='success',
            data=res
        )
        

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