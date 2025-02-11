from pydantic import BaseModel, Field, validator
from typing import Optional, List

#



class ProductColorRead(BaseModel):
    id: int
    color_id: int 
    name: Optional[str] = None
    slides: Optional[str] = None
    is_available: Optional[bool] = None
    sizes: List[int] = []

    class Config:
        orm_mode = True
        
        
class BaseStock(BaseModel):
    product_color_id: int
    size_id: int
    quantity: int

    class Config:
        orm_mode = True


class BaseCategory(BaseModel):
    title_en: Optional[str] = None
    title_ru: Optional[str] = None
    title_ua: str
    description_en: Optional[str] = None
    description_ru: Optional[str] = None
    description_ua: Optional[str]
    is_available: Optional[bool] = True
    code: Optional[str]

    class Config:
        orm_mode = True


class BaseProduct(BaseModel):
    title_en: Optional[str] = None
    title_ru: Optional[str] = None
    title_ua: str
    is_available: Optional[bool] = True
    code: Optional[str] = None
    id_crm: Optional[str] = None
    description_en: Optional[str] = None
    description_ru: Optional[str] = None
    description_ua: Optional[str] = None
    fabric: Optional[str] = None
    avatar: Optional[str] = None
    video: Optional[str] = None
    price: int
    sale: Optional[bool] = False
    discount_value: Optional[int] = None
    size_chart_id: Optional[int] = None
    

    class Config:
        orm_mode = True


# Основная модель для продукта
class ProductRead(BaseModel):
    id: int
    category_id: int
    title_en: Optional[str] = None
    title_ru: Optional[str] = None
    title_ua: str
    is_available: bool
    avatar: Optional[str] = None
    video: Optional[str] = None
    code: str
    id_crm: Optional[str] = None
    description_en: Optional[str] = None
    description_ru: Optional[str] = None
    description_ua: Optional[str] = None
    fabric: Optional[str] = None
    price: float
    sale: Optional[bool]
    discount_value: Optional[float] = 0.0
    colors: List[ProductColorRead] = []
    size_chart_id: Optional[int] = None

    class Config:
        orm_mode = True
        
        
class ProductCreate(BaseProduct):
    category_id: int


class ProductUpdate(BaseProduct):
    title_en: Optional[str] = None
    title_ru: Optional[str] = None
    title_ua: Optional[str] = None
    is_available: Optional[bool] = None
    code: Optional[str] = None
    description_en: Optional[str] = None
    description_ru: Optional[str] = None
    description_ua: Optional[str] = None
    fabric: Optional[str] = None
    price: Optional[int] = None
    sale: Optional[bool] = None
    discount_value: Optional[int] = None
    category_id: Optional[int] = None
    size_chart_id: Optional[int] = None
    
    class Config:
        orm_mode = True        




class BaseProductColor(BaseModel):
    product_id: int
    color_id: int
    slides: Optional[str] = None
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



        
        
        
        
        
class ProductColorUpdate(BaseModel):
    color_id: int 
    slides: Optional[str] = None
    is_available: Optional[bool] = None
    sizes: List[int] 

    class Config:
        orm_mode = True

    @validator('sizes', pre=True)
    def parse_sizes(cls, value):
        if isinstance(value, str):
            try:
                # Попробуем преобразовать строку в список
                return list(map(int, value.split(',')))
            except ValueError:
                raise ValueError("Invalid format for sizes. Expected a list of integers.")
        elif isinstance(value, list):
            # Если уже список, проверим, что все элементы — числа
            if not all(isinstance(i, int) for i in value):
                raise ValueError("Invalid format for sizes. Expected a list of integers.")
            return value
        raise ValueError("Invalid format for sizes. Expected a list of integers.")

    class Config:
        orm_mode = True


class SizeRead(BaseSize):
    id: int
    value: str

    class Config:
        orm_mode = True


# Create-схемы
class StockCreate(BaseStock):
    pass


class CategoryCreate(BaseCategory):
    pass






# Update-схемы
class StockUpdate(BaseStock):
    product_color_id: Optional[int] = None
    size_id: Optional[int] = None
    quantity: Optional[int] = None


class CategoryUpdate(BaseCategory):
    title_en: Optional[str] = None
    title_ru: Optional[str] = None
    title_ua: Optional[str]
    description_en: Optional[str] = None
    description_ru: Optional[str] = None
    description_ua: Optional[str] = None
    is_available: Optional[bool] = None
    code: Optional[str] = None



    
class ProductColorCreate(BaseProductColor):
    product_id: int
    color_id: int    
    slides: Optional[str] = None
    sizes: List[int]

    class Config:
        orm_mode = True

    @validator('sizes', pre=True)
    def parse_sizes(cls, value):
        if isinstance(value, str):
            try:
                # Попробуем преобразовать строку в список
                return list(map(int, value.split(',')))
            except ValueError:
                raise ValueError("Invalid format for sizes. Expected a list of integers.")
        elif isinstance(value, list):
            # Если уже список, проверим, что все элементы — числа
            if not all(isinstance(i, int) for i in value):
                raise ValueError("Invalid format for sizes. Expected a list of integers.")
            return value
        raise ValueError("Invalid format for sizes. Expected a list of integers.")

class SizeCreate(BaseModel):
    value: str  # Название размера

    class Config:
        orm_mode = True


class SizeUpdate(BaseModel):
    value: Optional[str] = None  # Название размера (можно обновить)

    class Config:
        orm_mode = True



class ProductColorUpdate(BaseProductColor):
    product_id: Optional[int] = None
    color_id: Optional[int] = None
    avatar: Optional[str] = None
    slides: Optional[str] = None
    sizes: Optional[List[int]] = None
    is_available: Optional[bool] = None
    
    class Config:
        orm_mode = True

    @validator('sizes', pre=True)
    def parse_sizes(cls, value):
        if isinstance(value, str):
            try:
                # Попробуем преобразовать строку в список
                return list(map(int, value.split(',')))
            except ValueError:
                raise ValueError("Invalid format for sizes. Expected a list of integers.")
        elif isinstance(value, list):
            # Если уже список, проверим, что все элементы — числа
            if not all(isinstance(i, int) for i in value):
                raise ValueError("Invalid format for sizes. Expected a list of integers.")
            return value
        raise ValueError("Invalid format for sizes. Expected a list of integers.")


class SizeUpdate(BaseSize):
    value: Optional[str] = None


class ColorRead(BaseModel):
    id: int
    name: str
    code: Optional[str] = None  # Код цвета может быть необязательным

    class Config:
        orm_mode = True

# Модель для создания
class ColorCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)  # Обязательное поле
    code: Optional[str] = Field(None, max_length=10)  # HEX код может быть длиной до 7 символов (#RRGGBB)

# Модель для обновления
class ColorUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)  # Обновление имени
    code: Optional[str] = Field(None, max_length=10)  # Обновление кода цвета
    
    
    
    
# Базовая схема для создания и обновления
class SizeChartBase(BaseModel):
    title: str
    table: str

# Схема для создания (наследуем от базовой)
class SizeChartCreate(SizeChartBase):
    pass

# Схема для обновления (делаем все поля опциональными)
class SizeChartUpdate(BaseModel):
    title: Optional[str] = None
    table: Optional[str] = None

# Схема для чтения
class SizeChartRead(SizeChartBase):
    id: int

    class Config:
        orm_mode = True
