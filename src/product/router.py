from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Product
from .schemas import ProductCreate, ProductRead
from database import get_async_session

from .models import Category, Product, ProductColor, ProductSize
from .schemas import CategoryRead, ProductCreate
from typing import List
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload


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
    new_product = Product(**product_data.model_dump())
    
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





@router.get("/products", response_model=List[ProductRead])
async def get_products(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_async_session),
):
    offset = (page - 1) * per_page
    
    # Запрос продуктов с предзагрузкой цветов и размеров
    query = (
        select(Product)
        .options(
            joinedload(Product.product_colors).joinedload(ProductColor.color),
            joinedload(Product.product_colors).joinedload(ProductColor.product_sizes),
        )
        .offset(offset)
        .limit(per_page)
    )
    result = await session.execute(query)
    
    # Используем unique() для устранения дублирования
    products = result.unique().scalars().all()

    # Преобразование данных
    product_list = []
    for product in products:
        colors: Dict[str, Dict] = {}
        for color in product.product_colors:
            colors[color.color.name] = {
                "avatar": color.avatar,
                "slides": color.slides.split(",") if color.slides else [],
                "video": color.video,
                "is_available": color.is_available,
                "sizes": [
                    {"id": size.id, "value": size.size.value, "quantity": size.quantity}
                    for size in color.product_sizes
                ],
            }

        product_data = {
            "id": product.id,
            "title_en": product.title_en,
            "title_ru": product.title_ru,
            "title_ua": product.title_ua,
            "title_tr": product.title_tr,
            "is_available": product.is_available,
            "code": product.code,
            "description_en": product.description_en,
            "description_ru": product.description_ru,
            "description_ua": product.description_ua,
            "description_tr": product.description_tr,
            "price": product.price,
            "sale": product.sale,
            "discount_value": product.discount_value,
            "category_id": product.category_id,
            "colors": colors,
        }

        product_list.append(product_data)

    return product_list
