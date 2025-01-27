from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Product
from .schemas import ProductCreate, ProductRead
from database import get_async_session
from auth.base_config import current_user
from .models import Category, Product, ProductColor
from .schemas import CategoryRead, ProductCreate
from typing import Dict, List
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from auth.roles import role, permission, Perms
from auth.models import User, Roles
from sqlalchemy.orm import selectinload



router = APIRouter(
                    prefix='/products',
                    tags=['Products']
                    )



@router.post("/add-product")
@role([Roles.admin.value, Roles.moderator.value])
async def add_product(        
        product_data: ProductCreate, 
        user: User = Depends(current_user),
        db: AsyncSession = Depends(get_async_session)
        ):
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

    # Строим запрос с загрузкой связанных данных
    query = (
        select(Product)
        .options(
            selectinload(Product.product_colors).selectinload(ProductColor.color)
        )
        .offset(offset)
        .limit(per_page)
    )

    result = await session.execute(query)
    products = result.scalars().all()

    # Формируем список продуктов с полными данными о цветах
    product_list = [
        {
            "id": product.id,
            "title_en": product.title_en,
            "title_ru": product.title_ru,
            "title_ua": product.title_ua,
            "is_available": product.is_available,
            "avatar": product.avatar,
            "slides": product.slides,
            "code": product.code,
            "id_crm": product.id_crm,
            "description_en": product.description_en,
            "description_ru": product.description_ru,
            "description_ua": product.description_ua,
            "price": product.price,
            "sale": product.sale,
            "discount_value": product.discount_value,
            "category_id": product.category_id,
            "colors": [
                {
                    "id": color.id,  # ID записи в таблице `product_colors`
                    "color_id": color.color.id if color.color else None,  # ID цвета
                    "name": color.color.name if color.color else None,  # Название цвета
                    "avatar": color.avatar,  # URL аватара цвета
                    "slides": color.slides,  # URL слайдов цвета
                    "is_available": color.is_available,  # Доступность цвета
                    "sizes": color.sizes,  # Доступные размеры (массив JSON)
                }
                for color in product.product_colors
            ],
        }
        for product in products
    ]

    return product_list



# @router.get("/products", response_model=List[ProductRead])
# async def get_products(
#     page: int = Query(1, ge=1),
#     per_page: int = Query(20, ge=1, le=100),
#     session: AsyncSession = Depends(get_async_session),
# ):
#     # Рассчитываем смещение и лимит для пагинации
#     offset = (page - 1) * per_page

#     # Строим запрос с использованием selectinload для загрузки связанных данных
#     query = (
#         select(Product)
#         .options(
#             selectinload(Product.product_colors).selectinload(ProductColor.color),
#             selectinload(Product.product_colors).selectinload(ProductColor.product_sizes),
#         )
#         .offset(offset)
#         .limit(per_page)
#     )

#     # Выполняем запрос и ждем результат
#     result = await session.execute(query)

#     # Извлекаем уникальные продукты из результата
#     products = result.scalars().unique().all()

#     # Преобразуем данные в формат, необходимый для ответа
#     product_list = []
#     for product in products:
#         colors = []

#         # Обрабатываем информацию о цветах, если они существуют
#         if product.product_colors:
#             for color in product.product_colors:
#                 sizes = [
#                     {"id": size.id, "value": size.size.value, "quantity": size.quantity}
#                     for size in color.product_sizes
#                 ]
#                 colors.append({
#                     "name": color.color.name if color.color else None,
#                     "avatar": color.avatar,
#                     "slides": color.slides if color.slides else '',
#                     "is_available": color.is_available,
#                     "sizes": sizes,
#                 })

#         # Формируем данные о продукте
#         product_data = {
#             "id": product.id,
#             "title_en": product.title_en,
#             "title_ru": product.title_ru,
#             "title_ua": product.title_ua,
#             "is_available": product.is_available,
#             "avatar": product.avatar,
#             "slides": product.slides,
#             "code": product.code,
#             "id_crm": product.id_crm,
#             "description_en": product.description_en,
#             "description_ru": product.description_ru,
#             "description_ua": product.description_ua,
#             "price": product.price,
#             "sale": product.sale,
#             "discount_value": product.discount_value,
#             "category_id": product.category_id,
#             "colors": colors,  # Список цветов с данными
#         }

#         product_list.append(product_data)

#     # Возвращаем список продуктов
#     return product_list