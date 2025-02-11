from fastapi import APIRouter, HTTPException, Query, Depends, Path
from sqlalchemy import exists, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Product
from .schemas import ColorCreate, ColorRead, ColorUpdate, ProductColorCreate, ProductColorRead, ProductCreate, ProductRead, SizeCreate, SizeUpdate
from database import get_async_session
from auth.base_config import current_user
from .models import Category, Product, ProductColor, Size, Color, SizeChart
from .schemas import CategoryRead, ProductCreate, SizeRead, ProductUpdate, ProductColorUpdate, ProductColorRead, SizeChartRead, SizeChartCreate, SizeChartUpdate
from typing import Dict, List
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from auth.roles import role, permission, Perms
from auth.models import User, Roles
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.attributes import flag_modified

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



@router.post("/update-product/{product_id}")
@role([Roles.admin.value, Roles.moderator.value])
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_async_session)
):
    # Найти продукт по ID
    result = await db.execute(select(Product).where(Product.id == product_id).options(joinedload(Product.category)))
    product = result.scalars().first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Обновить только те поля, которые переданы
    for key, value in product_data.dict(exclude_unset=True).items():
        setattr(product, key, value)

    # Сохранить изменения
    await db.commit()
    await db.refresh(product)

    return {"message": "Product updated successfully", "product": product}



@router.post("/add-color", response_model=ProductColorRead)
@role([Roles.admin.value, Roles.moderator.value])
async def add_color(
    payload: ProductColorCreate,
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_async_session),
):
    # Проверка существования продукта
    query = select(Product).where(Product.id == payload.product_id)
    product = await db.scalar(query)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Проверка существования цвета
    query = select(Color).where(Color.id == payload.color_id)
    color = await db.scalar(query)
    if not color:
        raise HTTPException(status_code=404, detail="Color not found")

    new_product_color = ProductColor(
        product_id=payload.product_id,
        color_id=payload.color_id,
        sizes=payload.sizes,
        is_available=payload.is_available,
        slides=payload.slides,
    )

    db.add(new_product_color)
    await db.commit()
    await db.refresh(new_product_color)

    # Создание объекта для ответа
    return ProductColorRead(
        id=new_product_color.id,
        color_id=new_product_color.color_id,
        name=color.name,  # Извлекаем имя цвета
        slides=new_product_color.slides,
        is_available=new_product_color.is_available,  # Если такое поле есть
        sizes=new_product_color.sizes,
    )




@router.post("/update-color/{color_id}", response_model=ProductColorRead)
@role([Roles.admin.value, Roles.moderator.value])
async def update_color(
    color_id: int,
    payload: ProductColorUpdate,
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_async_session),
):
    result = await db.execute(select(ProductColor).where(ProductColor.id == int(color_id)))
    product_color = result.scalar_one_or_none()
    
    if not product_color:
        raise HTTPException(status_code=404, detail="Color not found")

    update_data = payload.dict(exclude_unset=True)

    # Логируем, какие данные передаются
    print(f"Updating color_id {color_id} with data: {update_data}")

    for key, value in update_data.items():
        setattr(product_color, key, value)

    # **Явно устанавливаем sizes**
    if "sizes" in update_data:
        product_color.sizes = update_data["sizes"]
        flag_modified(product_color, "sizes") 
        print(f"Updated sizes: {product_color.sizes}")

    # Принудительное обновление состояния
    db.add(product_color)  # Указываем, что объект изменен
    await db.commit()
    await db.refresh(product_color)

    return product_color





@router.get("/products", response_model=List[ProductRead])
async def get_products(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=500),
    session: AsyncSession = Depends(get_async_session),
):
    offset = (page - 1) * per_page

    # Строим запрос с загрузкой связанных данных
    query = (
        select(Product)
        .options(
            selectinload(Product.product_colors).selectinload(ProductColor.color)
        )
        .order_by(Product.id.asc())
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
            "video": product.video,
            "code": product.code,
            "id_crm": product.id_crm,
            "description_en": product.description_en,
            "description_ru": product.description_ru,
            "description_ua": product.description_ua,
            "price": product.price,
            "sale": product.sale,
            "discount_value": product.discount_value,
            "category_id": product.category_id,
            "size_chart_id": product.size_chart_id,
            "fabric": product.fabric,
            "colors": [
                {
                    "id": color.id,  # ID записи в таблице `product_colors`
                    "color_id": color.color.id if color.color else None,  # ID цвета
                    "name": color.color.name if color.color else None,  # Название цвета
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


@router.get("/product/{product_id}", response_model=ProductRead)
async def get_product_by_id(
    product_id: int = Path(..., title="ID of the product", ge=1),
    session: AsyncSession = Depends(get_async_session),
):
    # Строим запрос с загрузкой связанных данных
    query = (
        select(Product)
        .options(
            selectinload(Product.product_colors).selectinload(ProductColor.color)
        )
        .where(Product.id == product_id)
    )

    result = await session.execute(query)
    product = result.scalars().first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Формируем структуру продукта с полными данными о цветах
    product_data = {
        "id": product.id,
        "title_en": product.title_en,
        "title_ru": product.title_ru,
        "title_ua": product.title_ua,
        "is_available": product.is_available,
        "avatar": product.avatar,
        "video": product.video,
        "code": product.code,
        "id_crm": product.id_crm,
        "description_en": product.description_en,
        "description_ru": product.description_ru,
        "description_ua": product.description_ua,
        "price": product.price,
        "sale": product.sale,
        "discount_value": product.discount_value,
        "category_id": product.category_id,
        "size_chart_id": product.size_chart_id,
        "fabric": product.fabric,
        "colors": [
            {
                "id": color.id,  # ID записи в таблице `product_colors`
                "color_id": color.color.id if color.color else None,  # ID цвета
                "name": color.color.name if color.color else None,  # Название цвета
                "slides": color.slides,  # URL слайдов цвета
                "is_available": color.is_available,  # Доступность цвета
                "sizes": color.sizes,  # Доступные размеры (массив JSON)
            }
            for color in product.product_colors
        ],
    }

    return product_data




@router.get("/product-color/{color_id}", response_model=ProductColorRead)
async def get_product_color_by_id(
    color_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    query = select(ProductColor).where(ProductColor.id == color_id)
    result = await session.execute(query)
    product_color = result.scalar_one_or_none()

    if product_color is None:
        raise HTTPException(status_code=404, detail="Product color not found")

    return ProductColorRead(
        id=product_color.id,
        color_id=product_color.color_id,
        slides=product_color.slides,  # Передаём как строку
        is_available=product_color.is_available,
        sizes=product_color.sizes,
    )


@router.delete("/products/{product_id}", response_model=dict)
@role([Roles.admin.value, Roles.moderator.value])
async def delete_product(
    product_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        # Проверяем, существует ли продукт с указанным ID
        result = await session.execute(
            select(Product).options(joinedload(Product.product_colors)).filter(Product.id == product_id)
        )
        product = result.scalars().first()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # Удаляем связанные ProductColor
        for color in product.product_colors:
            await session.delete(color)

        # Удаляем сам продукт
        await session.delete(product)

        # Применяем изменения
        await session.commit()

        return {"message": "Product deleted successfully"}

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete product due to database constraints")
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    
    
@router.delete("/product-colors/{color_id}", status_code=204)
@role([Roles.admin.value, Roles.moderator.value])
async def delete_product_color(color_id: int, 
                               user: User = Depends(current_user),
                               session: AsyncSession = Depends(get_async_session)):
    """
    Удаляет цвет продукта по его ID.
    """
    # Проверяем, существует ли запись цвета продукта
    result = await session.execute(select(ProductColor).where(ProductColor.id == color_id))
    product_color = result.scalars().first()

    if not product_color:
        raise HTTPException(status_code=404, detail="Product color not found")

    # Удаляем цвет продукта
    await session.delete(product_color)
    await session.commit()
    return {"message": f"Product color with ID {color_id} deleted successfully"}



















@router.get("/get-categories", response_model=List[CategoryRead])
async def get_all_categories(session: AsyncSession = Depends(get_async_session)):
    """
    Возвращает все категории.
    """
    query = select(Category)
    result = await session.execute(query)
    categories = result.scalars().all()
    return categories




@router.get("/get-sizes", response_model=List[SizeRead])
async def get_all_sizes(session: AsyncSession = Depends(get_async_session)):
    """
    Возвращает все размеры.
    """
    query = select(Size)
    result = await session.execute(query)
    sizes = result.scalars().all()
    return sizes


@router.post("/add-size", response_model=SizeRead)
@role([Roles.admin.value, Roles.moderator.value])
async def add_size(
    payload: SizeCreate,
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_async_session),
):
    # Создание нового размера
    new_size = Size(value=payload.value)

    db.add(new_size)
    await db.commit()
    await db.refresh(new_size)

    return SizeRead(id=new_size.id, value=new_size.value)



@router.post("/update-size/{size_id}", response_model=SizeRead)
@role([Roles.admin.value, Roles.moderator.value])
async def update_size(
    size_id: int,
    payload: SizeUpdate,
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_async_session),
):
    # Проверка существования размера
    query = select(Size).where(Size.id == size_id)
    size = await db.scalar(query)
    if not size:
        raise HTTPException(status_code=404, detail="Size not found")

    # Обновление данных размера
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(size, key, value)

    # Сохраняем изменения
    await db.commit()
    await db.refresh(size)

    return SizeRead(id=size.id, value=size.value)


@router.delete("/delete-size/{size_id}", status_code=200)
@role([Roles.admin.value, Roles.moderator.value])
async def delete_size(
    size_id: int,
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_async_session),
):
    # Поиск размера в базе
    result = await db.execute(select(Size).where(Size.id == size_id))
    size = result.scalars().first()

    if not size:
        return {"detail": "Размер не найден"}

    try:
        # Удаление размера (без проверок)
        await db.delete(size)
        await db.commit()

        return {"detail": "Размер успешно удалён"}
    
    except Exception as e:
        # Возвращаем ошибку, если удаление не удалось
        return {"detail": str(e)}





@router.get("/get-colors", response_model=List[ColorRead])
async def get_all_sizes(session: AsyncSession = Depends(get_async_session)):
    """
    Возвращает все цвета.
    """
    query = select(Color)
    result = await session.execute(query)
    colors = result.scalars().all()
    return colors



@router.delete("/delete-color/{color_id}", status_code=200)
@role([Roles.admin.value, Roles.moderator.value])
async def delete_color(
    color_id: int,
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_async_session),
):
    # Поиск цвета в базе
    result = await db.execute(select(Color).where(Color.id == color_id))
    color = result.scalars().first()

    if not color:
        return {"detail": "Цвет не найден"}

    # Проверка привязан ли цвет к товарам
    # Например, делаем запрос, чтобы узнать, используется ли цвет в каких-либо товарах
    product_count = await db.execute(select(func.count()).where(ProductColor.color_id == color.id))
    product_count = product_count.scalar()

    if product_count > 0:
        return {"detail": "Цвет привязан к товарам, удаление невозможно"}

    # Удаление цвета
    await db.delete(color)
    await db.commit()

    return {"detail": "Цвет успешно удалён"}


@router.post("/edit-color/{color_id}", response_model=ColorUpdate)
@role([Roles.admin.value, Roles.moderator.value])
async def update_color(color_id: int, 
                       data: ColorUpdate, 
                       user: User = Depends(current_user),
                        db: AsyncSession = Depends(get_async_session)):
    
    print(f"Тип ID: {type(color_id)}, значение: {color_id}")
    result = await db.execute(select(Color).where(Color.id == color_id))
    color = result.scalars().first()
    
    if not color:
        raise HTTPException(status_code=404, detail="Цвет не найден")

    # Обновить только переданные поля
    if data.name is not None:
        color.name = data.name
    if data.code is not None:
        color.code = data.code

    await db.commit()
    await db.refresh(color)

    return color




@router.post("/create-color", status_code=201)
@role([Roles.admin.value, Roles.moderator.value])
async def create_color(
    color: ColorCreate,
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_async_session),
):
    # Проверяем, существует ли уже цвет с таким же названием или кодом
    existing_color = await db.execute(select(Color).filter(
        (Color.name == color.name) | (Color.code == color.code)
    ))
    existing_color = existing_color.scalars().first()

 
    new_color = Color(name=color.name, code=color.code)
    
    # Добавляем в базу данных
    db.add(new_color)
    await db.commit()

    return {"detail": "Цвет успешно создан", "color": new_color}




@router.get("/size-charts", response_model=list[SizeChartRead])
async def get_all_size_charts(session: AsyncSession = Depends(get_async_session)):
    query = select(SizeChart)
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/size-chart/{size_chart_id}", response_model=SizeChartRead)
async def get_size_chart(size_chart_id: int, session: AsyncSession = Depends(get_async_session)):
    size_chart = await session.get(SizeChart, size_chart_id)
    if not size_chart:
        raise HTTPException(status_code=404, detail="Size Chart not found")
    return size_chart


@router.post("/size-chart-add", response_model=SizeChartRead)
@role([Roles.admin.value, Roles.moderator.value])
async def create_size_chart(data: SizeChartCreate,
                            user: User = Depends(current_user),
                            session: AsyncSession = Depends(get_async_session)):
    new_size_chart = SizeChart(**data.dict())
    session.add(new_size_chart)
    await session.commit()
    await session.refresh(new_size_chart)
    return new_size_chart



@router.post("/size-chart-update/{size_chart_id}", response_model=SizeChartRead)
@role([Roles.admin.value, Roles.moderator.value])
async def update_size_chart(size_chart_id: int, 
                            data: SizeChartUpdate, 
                            user: User = Depends(current_user),
                            session: AsyncSession = Depends(get_async_session)):
    size_chart = await session.get(SizeChart, size_chart_id)
    if not size_chart:
        raise HTTPException(status_code=404, detail="Size Chart not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(size_chart, key, value)

    await session.commit()
    await session.refresh(size_chart)
    return size_chart


@router.delete("/size-chart-delete/{size_chart_id}")
@role([Roles.admin.value, Roles.moderator.value])
async def delete_size_chart(size_chart_id: int, 
                            user: User = Depends(current_user),
                            session: AsyncSession = Depends(get_async_session)):
    size_chart = await session.get(SizeChart, size_chart_id)
    if not size_chart:
        raise HTTPException(status_code=404, detail="Size Chart not found")

    await session.delete(size_chart)
    await session.commit()
    return {"message": "Size Chart deleted successfully"}
