from sqlalchemy import Column, Integer, String, TIMESTAMP, Enum, Float, Text, ForeignKey, JSON, BIGINT
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from orders.schemas import OrderStatus, DeliveryMethod, PaymentMethod, OrderUpdateStatus, TelegramNotification
from auth.models import User
from database import Base




class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    site_name = Column(String, ForeignKey('sites.site_name'), nullable=False)  # Привязка к таблице sites
    
    order_status = Column(Enum(OrderStatus), default=OrderStatus.received, nullable=False)
    telegram_notification = Column(Enum(TelegramNotification), default=TelegramNotification.waiting, nullable=False)
    
    
    client_phone = Column(String, nullable=False)
    client_name = Column(String, nullable=True)
    client_email = Column(String, nullable=True)
    client_city = Column(String, nullable=True)
    client_address = Column(String, nullable=True)
    
    delivery_method = Column(Enum(DeliveryMethod), nullable=True)
    
    payment_method = Column(Enum(PaymentMethod), default=PaymentMethod.cash, nullable=False)
    payment_id = Column(Integer, nullable=True)  # ID оплаты, nullable, если нет необходимости
    
    product_name = Column(String, nullable=True)
    product_type = Column(String, nullable=True)
    product_color = Column(String, nullable=True)
    product_size = Column(String, nullable=True)
    product_quantity = Column(Integer, nullable=True)

    price_product = Column(Float, nullable=True)
    price_taxes = Column(Float, nullable=True)
    price_delivery = Column(Float, nullable=True)
    price_total = Column(Float, nullable=True)

    notes = Column(Text, nullable=True)
    received = Column(TIMESTAMP, default=func.now(), nullable=False)
    client_ip = Column(String, nullable=True)

    site = relationship('Site', back_populates='orders')


class Site(Base):
    __tablename__ = 'sites'
    
    id = Column(Integer, primary_key=True)
    site_name = Column(String, unique=True, nullable=False)
    site_domain = Column(String, nullable=True)
    site_owner = Column(Integer)  # Связь с пользователем (User.id)
    owner_telegram = Column(String, nullable=True)  # Телеграм ID владельца сайта
    owner_email = Column(String, nullable=True)
    site_description = Column(String, nullable=True)
    site_category = Column(String, nullable=True)
        
    orders = relationship('Order', back_populates='site')  # Связь с таблицей orders


class SiteAdmins(Base):
    __tablename__ = 'sites_admins'
    
    id = Column(Integer, primary_key=True)
    site_name = Column(String, ForeignKey('sites.site_name'), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    role = Column(String, nullable=False)


class OrderUpdatesLogs(Base):
    __tablename__ = 'order_updates_logs'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)  # Кто сделал изменение
    order_id = Column(Integer, ForeignKey(Order.id), nullable=False)  # Какой заказ был обновлен
    previous_state = Column(JSON, nullable=False)  # Предыдущее состояние заказа (JSON)
    current_state = Column(JSON, nullable=False)   # Текущее состояние заказа (JSON)
    update_time = Column(TIMESTAMP, default=func.now(), nullable=False)  # Время обновления
    status = Column(Enum(OrderUpdateStatus), default=OrderUpdateStatus.posted)
