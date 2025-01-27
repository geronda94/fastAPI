from pydantic import BaseModel
from typing import Optional, List

# Базовые схемы
class BaseStock(BaseModel):
    product_color_id: int
    size_id: int
    quantity: int

    class Config:
        orm_mode = True


class BaseCategory(BaseModel):
    title_en: str
    title_ru: str
    title_ua: str
    description_en: Optional[str]
    description_ru: Optional[str]
    description_ua: Optional[str]
    is_available: Optional[bool] = True
    code: Optional[str]

    class Config:
        orm_mode = True


class BaseProduct(BaseModel):
    title_en: str
    title_ru: Optional[str]
    title_ua: Optional[str]
    is_available: Optional[bool] = True
    code: Optional[str]
    id_crm: Optional[str]
    description_en: Optional[str]
    description_ru: Optional[str]
    description_ua: Optional[str]
    avatar: Optional[str]
    slides: Optional[str]
    price: int
    sale: Optional[bool] = False
    discount_value: Optional[int]

    class Config:
        orm_mode = True


class BaseProductColor(BaseModel):
    product_id: int
    color_id: int
    avatar: Optional[str]
    slides: Optional[str]
    is_available: Optional[bool] = True

    class Config:
        orm_mode = True


class BaseSize(BaseModel):
    value: str

    class Config:
        orm_mode = True


# Read-схемы
class StockRead(BaseStock):
    id: int

    class Config:
        orm_mode = True


class CategoryRead(BaseCategory):
    id: int

    class Config:
        orm_mode = True




class ProductColorSizeRead(BaseModel):
    id: int
    value: str
    quantity: int

    class Config:
        orm_mode = True


class ProductColorRead(BaseModel):
    id: int
    color_id: int 
    name: str
    avatar: Optional[str] = None
    slides: Optional[str] = None
    is_available: Optional[bool] = None
    sizes: List[int] = []

    class Config:
        orm_mode = True

# Основная модель для продукта
class ProductRead(BaseModel):
    id: int
    category_id: int
    title_en: str
    title_ru: str
    title_ua: str
    is_available: bool
    avatar: Optional[str] = None
    slides: Optional[str] = None
    code: str
    id_crm: Optional[str] = None
    description_en: Optional[str] = None
    description_ru: Optional[str] = None
    description_ua: Optional[str] = None
    price: float
    sale: Optional[float] = 0.0
    discount_value: Optional[float] = 0.0
    colors: List[ProductColorRead] = []

    class Config:
        orm_mode = True



class SizeRead(BaseSize):
    id: int

    class Config:
        orm_mode = True


# Create-схемы
class StockCreate(BaseStock):
    pass


class CategoryCreate(BaseCategory):
    pass


class ProductCreate(BaseProduct):
    category_id: int


class ProductColorCreate(BaseProductColor):
    pass


class SizeCreate(BaseSize):
    pass


# Update-схемы
class StockUpdate(BaseStock):
    product_color_id: Optional[int]
    size_id: Optional[int]
    quantity: Optional[int]


class CategoryUpdate(BaseCategory):
    title_en: Optional[str]
    title_ru: Optional[str]
    title_ua: Optional[str]
    description_en: Optional[str]
    description_ru: Optional[str]
    description_ua: Optional[str]
    is_available: Optional[bool]
    code: Optional[str]


class ProductUpdate(BaseProduct):
    title_en: Optional[str]
    title_ru: Optional[str]
    title_ua: Optional[str]
    is_available: Optional[bool]
    code: Optional[str]
    description_en: Optional[str]
    description_ru: Optional[str]
    description_ua: Optional[str]
    price: Optional[int]
    sale: Optional[bool]
    discount_value: Optional[int]
    category_id: Optional[int]


class ProductColorUpdate(BaseProductColor):
    product_id: Optional[int]
    color_id: Optional[int]
    avatar: Optional[str]
    slides: Optional[str]
    is_available: Optional[bool]


class SizeUpdate(BaseSize):
    value: Optional[str]

