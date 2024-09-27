from enum import Enum

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