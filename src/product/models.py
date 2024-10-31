from sqlalchemy import Column, ForeignKey, String, Boolean, Integer, Text
from sqlalchemy.orm import relationship
from database import Base



class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    title_en = Column(String, nullable=False)
    title_ru = Column(String, nullable=False)
    title_ua = Column(String, nullable=False)
    title_tr = Column(String, nullable=False)
    description_en = Column(Text, nullable=True)
    description_ru = Column(Text, nullable=True)
    description_ua = Column(Text, nullable=True)
    description_tr = Column(Text, nullable=True)
    is_available = Column(Boolean, default=True)
    code = Column(String, nullable=True)    
    
    products = relationship("Product", back_populates="category")
    
    
    
class Color(Base):
    __tablename__ = 'colors'

    id = Column(Integer, primary_key=True, index=True)
    value = Column(String, nullable=False)
    code = Column(String, nullable=True)

    types = relationship("Type", back_populates="color")



class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    order_status = Column(String, nullable=False)  # Enum mapping can be added
    country = Column(String, nullable=True)
    city = Column(String, nullable=True)
    address = Column(String, nullable=True)
    delivery_method = Column(String, nullable=False)  # Enum mapping can be added
    payment_method = Column(String, nullable=False)  # Enum mapping can be added
    total_price = Column(Integer, nullable=False)

    order_items = relationship("OrderItem", back_populates="order")



class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    type_id = Column(Integer, ForeignKey('types.id'))
    quantity = Column(Integer, nullable=False)
    price_per_unit = Column(Integer, nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id'))

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product")
    type = relationship("Type")
    
    
    
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    title_en = Column(String, nullable=False)
    title_ru = Column(String, nullable=True)
    title_ua = Column(String, nullable=True)
    title_tr = Column(String, nullable=True)
    is_available = Column(Boolean, default=True)
    code = Column(String, nullable=True)
    description_en = Column(Text, nullable=True)
    description_ru = Column(Text, nullable=True)
    description_ua = Column(Text, nullable=True)
    description_tr = Column(Text, nullable=True)
    price = Column(Integer, nullable=False)
    sale = Column(Boolean, default=False)
    discount_value = Column(Integer, nullable=True)  
    

     # Поля для хранения ссылок на аватар, слайды и видео
    avatar = Column(String, nullable=True)  # URL ссылки на аватар
    slides = Column(String, nullable=True)  # URL ссылки на слайды (может быть строка с разделителем, если несколько)
    video = Column(String, nullable=True)   # URL ссылки на видео
    
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category", back_populates="products")

    types = relationship("Type", back_populates="product")



class Size(Base):
    __tablename__ = 'sizes'

    id = Column(Integer, primary_key=True, index=True)
    value = Column(String, nullable=False)

    types = relationship("Type", back_populates="size")



class Type(Base):
    __tablename__ = 'types'

    id = Column(Integer, primary_key=True, index=True)
    size_id = Column(Integer, ForeignKey('sizes.id'))
    color_id = Column(Integer, ForeignKey('colors.id'))
    is_available = Column(Boolean, default=True)
    remainder = Column(Integer, nullable=True)
    quantity = Column(String, nullable=False)

    size = relationship("Size", back_populates="types")
    color = relationship("Color", back_populates="types")
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship("Product", back_populates="types")
