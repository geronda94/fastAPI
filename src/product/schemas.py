from pydantic import BaseModel, Field
from typing import Optional, List


class BaseCategory(BaseModel):
    title_en: str
    title_ru: str
    title_ua: str
    title_tr: str
    description_en: Optional[str]
    description_ru: Optional[str]
    description_ua: Optional[str]
    description_tr: Optional[str]
    is_available: Optional[bool] = True
    code: Optional[str]


class BaseProduct(BaseModel):
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


class BaseProductColor(BaseModel):
    product_id: int
    color_id: int
    avatar: Optional[str]
    slides: Optional[str]
    video: Optional[str]
    is_available: Optional[bool] = True


class BaseSize(BaseModel):
    value: str


class BaseProductSize(BaseModel):
    product_color_id: int
    size_id: int
    quantity: int


class BaseOrder(BaseModel):
    name: str
    email: str
    phone: str
    order_status: str
    country: Optional[str]
    city: Optional[str]
    address: Optional[str]
    delivery_method: str
    payment_method: str
    total_price: int


class BaseOrderItem(BaseModel):
    product_id: int
    product_color_id: int
    product_syze_id: int
    quantity: int
    price_per_unit: int
    order_id: int






class CategoryRead(BaseCategory):
    id: int

    class Config:
        orm_mode = True


class ProductRead(BaseProduct):
    id: int
    category_id: int

    class Config:
        orm_mode = True


class ProductColorRead(BaseProductColor):
    id: int

    class Config:
        orm_mode = True


class SizeRead(BaseSize):
    id: int

    class Config:
        orm_mode = True


class ProductSizeRead(BaseProductSize):
    id: int

    class Config:
        orm_mode = True


class OrderRead(BaseOrder):
    id: int

    class Config:
        orm_mode = True


class OrderItemRead(BaseOrderItem):
    id: int

    class Config:
        orm_mode = True







class CategoryCreate(BaseCategory):
    pass


class ProductCreate(BaseProduct):
    category_id: int


class ProductColorCreate(BaseProductColor):
    pass


class SizeCreate(BaseSize):
    pass


class ProductSizeCreate(BaseProductSize):
    pass


class OrderCreate(BaseOrder):
    pass


class OrderItemCreate(BaseOrderItem):
    pass









class CategoryUpdate(BaseCategory):
    title_en: Optional[str]
    title_ru: Optional[str]
    title_ua: Optional[str]
    title_tr: Optional[str]
    description_en: Optional[str]
    description_ru: Optional[str]
    description_ua: Optional[str]
    description_tr: Optional[str]
    is_available: Optional[bool]
    code: Optional[str]


class ProductUpdate(BaseProduct):
    title_en: Optional[str]
    title_ru: Optional[str]
    title_ua: Optional[str]
    title_tr: Optional[str]
    is_available: Optional[bool]
    code: Optional[str]
    description_en: Optional[str]
    description_ru: Optional[str]
    description_ua: Optional[str]
    description_tr: Optional[str]
    price: Optional[int]
    sale: Optional[bool]
    discount_value: Optional[int]
    category_id: Optional[int]


class ProductColorUpdate(BaseProductColor):
    product_id: Optional[int]
    color_id: Optional[int]
    avatar: Optional[str]
    slides: Optional[str]
    video: Optional[str]
    is_available: Optional[bool]


class SizeUpdate(BaseSize):
    value: Optional[str]


class ProductSizeUpdate(BaseProductSize):
    product_color_id: Optional[int]
    size_id: Optional[int]
    quantity: Optional[int]


class OrderUpdate(BaseOrder):
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    order_status: Optional[str]
    country: Optional[str]
    city: Optional[str]
    address: Optional[str]
    delivery_method: Optional[str]
    payment_method: Optional[str]
    total_price: Optional[int]


class OrderItemUpdate(BaseOrderItem):
    product_id: Optional[int]
    product_color_id: Optional[int]
    product_syze_id: Optional[int]
    quantity: Optional[int]
    price_per_unit: Optional[int]
    order_id: Optional[int]
