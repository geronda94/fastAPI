from sqlalchemy import Column, ForeignKey, String, Boolean, Integer, Text, JSON
from sqlalchemy.orm import relationship
from database import Base

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    title_en = Column(String, nullable=True)
    title_ru = Column(String, nullable=True)
    title_ua = Column(String, nullable=False)
    description_en = Column(Text, nullable=True)
    description_ru = Column(Text, nullable=True)
    description_ua = Column(Text, nullable=True)
    is_available = Column(Boolean, default=True)
    code = Column(String, nullable=True)

    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    title_en = Column(String, nullable=True)
    title_ru = Column(String, nullable=True)
    title_ua = Column(String, nullable=False)
    is_available = Column(Boolean, default=True)
    code = Column(String, nullable=True)
    id_crm = Column(String, nullable=True)
    description_en = Column(Text, nullable=True)
    description_ru = Column(Text, nullable=True)
    description_ua = Column(Text, nullable=True)
    fabric = Column(Text, nullable=True)
    price = Column(Integer, nullable=False)  # Цена (оставлено как Integer)
    sale = Column(Boolean, default=False)
    discount_value = Column(Integer, nullable=True)
    avatar = Column(String, nullable=True)  # URL аватара
    video = Column(String, nullable=True)  # URL аватара
    category_id = Column(Integer, ForeignKey('categories.id'))        
    size_chart_id = Column(Integer, ForeignKey('size_chart.id'), nullable=True)  
    

    category = relationship("Category", back_populates="products")
    product_colors = relationship("ProductColor", back_populates="product")


class ProductColor(Base):
    __tablename__ = 'product_colors'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    color_id = Column(Integer, ForeignKey('colors.id'), nullable=False)
    avatar = Column(String, nullable=True)  # URL аватара
    slides = Column(String, nullable=True)  # URL слайдов (через запятую)
    is_available = Column(Boolean, default=True)
    sizes = Column(JSON, nullable=True)  # Список доступных размеров (массив идентификаторов из таблицы Sizes)
    product = relationship("Product", back_populates="product_colors")
    color = relationship("Color", back_populates="product_colors")


class Color(Base):
    __tablename__ = 'colors'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Название цвета
    code = Column(String, nullable=True)  # Код цвета (RGB или HEX)

    product_colors = relationship("ProductColor", back_populates="color")


class Size(Base):
    __tablename__ = 'sizes'

    id = Column(Integer, primary_key=True, index=True)
    value = Column(String, nullable=False)  # Название размера




# class Stock(Base):  # Эта таблица будет использоваться позже для хранения остатков
#     __tablename__ = 'stocks'

#     id = Column(Integer, primary_key=True, index=True)
#     product_color_id = Column(Integer, ForeignKey('product_colors.id'), nullable=False)
#     size_id = Column(Integer, ForeignKey('sizes.id'), nullable=False)
#     quantity = Column(Integer, nullable=False)  # Количество товара на складе

#     product_color = relationship("ProductColor", back_populates="stocks")
#     size = relationship("Size", back_populates="stocks")


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    order_status = Column(String, nullable=False)  # Статус заказа (можно добавить Enum позже, если нужно)
    country = Column(String, nullable=True)
    city = Column(String, nullable=True)
    address = Column(String, nullable=True)
    total_price = Column(Integer, nullable=False)

    order_items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    product_color_id = Column(Integer, ForeignKey('product_colors.id'))  # Связь с ProductColor
    quantity = Column(Integer, nullable=False)
    price_per_unit = Column(Integer, nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id'))

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product")
    product_color = relationship("ProductColor")



class SizeChart(Base):
    __tablename__ = 'size_chart'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    table = Column(String, nullable=False)