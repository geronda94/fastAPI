from pydantic import BaseModel, Field
from typing import Optional, List


class ProductBase(BaseModel):
    title_en: str
    title_ru: Optional[str]
    title_ua: Optional[str]
    title_tr: Optional[str]
    is_available: Optional[bool] = True
    code: Optional[str]
    description_en: Optional[str]
    description_ru: Optional[str]
    description_ua: Optional[str]
    description_tr: Optional[str]
    price: int
    sale: Optional[bool] = False
    discount_value: Optional[int]
    avatar: Optional[str]
    slides: Optional[str]
    video: Optional[str]
    category_id: int


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int

    class Config:
        orm_mode = True


