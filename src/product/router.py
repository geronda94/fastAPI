from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Product
from .schemas import ProductCreate, ProductRead
from database import get_async_session

from .models import Category, Product
from .schemas import CategoryRead, ProductCreate
from typing import List

router = APIRouter(
                    prefix='/products',
                    tags=['Products']
                    )



@router.post("/add-product")
async def add_product(product_data: ProductCreate, db: AsyncSession = Depends(get_async_session)):
    # Проверка на существование категории
    category = await db.execute(select(Category).where(Category.id == product_data.category_id))
    category = category.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Создание нового продукта
    new_product = Product(**product_data.dict())
    
    # Сохранение в базе данных
    try:
        db.add(new_product)
        await db.commit()
        await db.refresh(new_product)
    except Exception as ex:
        print(ex)
    
    return {"message": "Product added successfully", "product": new_product}




@router.get("/get-categories", response_model=List[CategoryRead])
async def get_all_categories(session: AsyncSession = Depends(get_async_session)):
    """
    Возвращает все категории.
    """
    query = select(Category)
    result = await session.execute(query)
    categories = result.scalars().all()
    return categories