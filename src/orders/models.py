from database import Base
from sqlalchemy import  Column, Integer, String, TIMESTAMP, Enum, Float, Text
from .schemas import OrderStatus, DeliveryMethod, PaymentMethod



class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    site = Column(String)
    status = Column(Enum(OrderStatus), default=OrderStatus.received, nullable=False)
    
    client_phone = Column(String)
    client_email = Column(String)
    client_city = Column(String)
    client_address = Column(String)
    delivery_method = Column(Enum(DeliveryMethod))
    
    payment_method = Column(Enum(PaymentMethod), default=PaymentMethod.cash)
    payment_id = Column(Integer)
    
    product_name = Column(String)
    product_type = Column(String)
    product_color = Column(String)
    product_size = Column(String)
    product_quantity = Column(Integer)
    
    price_product = Column(Float)
    price_taxes = Column(Float)
    price_delivery = Column(Float)
    price_total = Column(Float)
    
    notes = Column(Text)
    received = Column(TIMESTAMP)
    client_ip = Column(String)



