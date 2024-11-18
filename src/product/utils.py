from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

async def get_product_with_colors_and_sizes(session: AsyncSession, product_id: int):
    result = await session.execute(
        select(Product)
        .options(
            joinedload(Product.product_colors)  # Загружаем связанные цвета
            .joinedload(ProductColor.product_sizes)  # В каждом цвете загружаем размеры
            .joinedload(ProductSize.size)  # Для каждого размера получаем данные из таблицы Size
        )
        .where(Product.id == product_id)
    )
    product = result.scalars().first()
    return product



async def get_paginated_products(session: AsyncSession, page: int, page_size: int = 40):
    products = await get_products_with_pagination(session, page, page_size)
    return [ProductSchema.from_orm(product) for product in products]
