from starlette_admin.contrib.sqla import Admin, ModelView

from database import engine
from auth.models import User
from orders.models import Order, Site, SiteAdmins
from auth.base_config import current_user
from fastapi import Depends





  

admin = Admin(engine, title="Admin Panel")
admin.add_view(ModelView(User))
admin.add_view(ModelView(Order))
admin.add_view(ModelView(SiteAdmins))
admin.add_view(ModelView(Site))
# Добавляем Middleware

