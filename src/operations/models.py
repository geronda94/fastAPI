from sqlalchemy import Boolean, JSON, Integer, String, TIMESTAMP, ForeignKey, Column
from sqlalchemy.orm import relationship, declarative_base, validates
from datetime import datetime
import re

Base = declarative_base()


class Role(Base):
    __tablename__ = "role"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    permissions = Column(JSON)

    # Связь с пользователями
    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    role_id = Column(Integer, ForeignKey("role.id"))
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    # Связь с ролями
    role = relationship("Role", back_populates="users")
    
    @validates(email)
    def validate_email(self, key, address):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, address):
            raise ValueError("Invalid email address")
        return address





























# from sqlalchemy import Boolean, MetaData, JSON, Table, Column, Integer, String, TIMESTAMP, ForeignKey 
# from datetime import datetime


# metadata = MetaData()

# role = Table(
#     "role",
#     metadata,
#     Column('id', Integer, primary_key=True),
#     Column('name', String, nullable=False),
#     Column('permissions', JSON)
# )

# user = Table(
#     'user',
#     metadata,
#     Column('id', Integer, primary_key=True),
#     Column('email', String, nullable=False),
#     Column('username', String, nullable=False),
#     Column('hashed_password', String, nullable=False),
#     Column('registred_at', TIMESTAMP, default=datetime.utcnow),
#     Column('role_id', Integer,  ForeignKey(role.c.id)),
#     Column('is_active', Boolean, default=True, nullable=False),
#     Column('is_superuser', Boolean, default=True, nullable=False),
#     Column('is_verified', Boolean, default=True, nullable=False)
# )

