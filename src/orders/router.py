from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .schemas import OrderCreate
from database import get_async_session
from .models import Order



router = APIRouter(
    prefix='/orders',
    tags=['Orders']
)

@router.post('/recieve')
async def recieve_order(order: OrderCreate, db: AsyncSession = Depends(get_async_session)):
    new_order = Order(**order.model_dump())
    try:
        db.add(new_order)
        await db.commit()
        await db.refresh(new_order)
            
        return 'success'
    
    except Exception as ex:
        raise HTTPException(403, str(ex))
