from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr

class OrderStatus(str, Enum):
    received = "received"
    accepted = "accepted"
    processed = "processed"
    confirmed = "confirmed"
    shipped = "shipped"
    delivered = "delivered"
    canceled = "canceled"



class DeliveryMethod(str, Enum):
    courier = 'Курьером'
    mail = 'Почтой'
    self = 'Самовывоз'
    
    
class PaymentMethod(str, Enum):
    cash = 'Наличными при получении'
    remittance = 'Денежный перевод'
    online = 'Оплата онлайн'
    
class OrderUpdateStatus(str, Enum):
    posted = 'posted'
    checked = 'checked'
    
    
    
    
    
    
class OrderCreate(BaseModel):
    site_name: str
    order_status: OrderStatus = OrderStatus.received
    client_phone: str
    client_email: Optional[EmailStr] = None
    client_city: str
    client_address: Optional[str] = None
    delivery_method: Optional[DeliveryMethod] = None
    payment_method: PaymentMethod = PaymentMethod.cash
    payment_id: Optional[int] = None
    product_name: str
    product_type: Optional[str] = None
    product_color: Optional[str] = None
    product_size: Optional[str] = None
    product_quantity: Optional[int] = None
    price_product: float
    price_taxes: Optional[float] = None
    price_delivery: Optional[float] = None
    price_total: Optional[float] = None
    notes: Optional[str] = None
    client_ip: Optional[str] = None

    class Config:
        orm_mode = True