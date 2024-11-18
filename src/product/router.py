from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Product
from .schemas import ProductCreate, ProductRead
from database import get_async_session

router = APIRouter(
                    prefix='/products',
                    tags=['Products']
                    )


@router.post("/create-product", response_model=ProductRead, status_code=201)
async def create_product(product: ProductCreate, session: AsyncSession = Depends(get_async_session)):
    db_product = Product(**product.dict())
    session.add(db_product)
    await session.commit()
    await session.refresh(db_product)
    return db_product

