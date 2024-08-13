from sqlalchemy import MetaData, JSON, Table, Column, Integer, String, TIMESTAMP, ForeignKey 
import datetime


metadata = MetaData()

roles = Table(
    "roles",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('permissions', JSON)
)

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('email', String, nullable=False),
    Column('username', String, nullable=False),
    Column('password', String, nullable=False),
    Column('registred_at', TIMESTAMP, default=datetime.datetime.utcnow),
    Column('role_id', Integer,  ForeignKey('roles.id')),
)