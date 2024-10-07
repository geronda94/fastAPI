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
    
    
class TelegramNotification(str, Enum):
    waiting = 'waiting'
    delivered = 'delivered'
    
    
    
    
class OrderCreate(BaseModel):
    site_name: str
    order_status: OrderStatus = OrderStatus.received.value
    telegram_notification: TelegramNotification = TelegramNotification.waiting.value
    client_phone: str
    client_email: EmailStr
    client_city: str | None = None
    client_address: str | None = None
    delivery_method: Optional[DeliveryMethod] = None
    payment_method: PaymentMethod = PaymentMethod.cash
    payment_id: Optional[int] = None  # Измените на Optional[int]
    product_name: str | None = None
    product_type: str | None = None
    product_color: str | None = None
    product_size: str | None = None
    product_quantity: Optional[int] = None
    price_product: float | None = None
    price_taxes: float | None = None
    price_delivery: float | None = None
    price_total: float | None = None
    notes: str | None = None
    client_ip: str | None = None

    class Config:
        from_attributes = True

        
 
class OrderRead(OrderCreate):
    id: int
    received: datetime  # Поле для даты получения заказа

    def format_message(self):
        # Преобразуем дату в читаемый формат
        formatted_date = self.received.strftime('%H:%M %d-%m-%Y')  # Например, 04-10-2024 22:11:25

        # Словарь для хранения сообщения
        message_data = {
            "ID": self.id,
            "Сайт": self.site_name,
            "Статус заказа": self.order_status,
            "Телефон клиента": self.client_phone,
            "Email клиента": self.client_email,
            "Город клиента": self.client_city,
            "Адрес клиента": self.client_address,
            "Метод доставки": self.delivery_method,
            "Метод оплаты": self.payment_method,
            "ID платежа": self.payment_id,
            "Название товара": self.product_name,
            "Тип товара": self.product_type,
            "Цвет товара": self.product_color,
            "Размер товара": self.product_size,
            "Количество товара": self.product_quantity,
            "Дата заказа": formatted_date,
        }

        # Удаляем пустые значения и поля с ценами равными 0.0
        formatted_message = "\n".join(
            f"{key}: {value}"
            for key, value in message_data.items()
            if value is not None and not (
                isinstance(value, (float, int)) and value == 0.0
            )
        )

        return formatted_message




    

class SiteCreate(BaseModel):
    site_name: str
    site_domain: str
    site_owner: int
    owner_telegram: Optional[str] = None
    site_description: Optional[str] = None
    site_category: Optional[str] = None



class SiteRead(BaseModel):
    id: int
    site_name: str
    site_domain: str
    site_owner: int
    owner_telegram: Optional[str] = None
    site_description: Optional[str] = None
    site_category: Optional[str] = None

    class Config:
        from_attributes = True 