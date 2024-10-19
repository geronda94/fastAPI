"""Initial migration

Revision ID: 9b6175ef29a6
Revises: 
Create Date: 2024-10-14 20:24:01.406391

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9b6175ef29a6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title_en', sa.String(), nullable=False),
    sa.Column('title_ru', sa.String(), nullable=False),
    sa.Column('title_ua', sa.String(), nullable=False),
    sa.Column('title_tr', sa.String(), nullable=False),
    sa.Column('description_en', sa.Text(), nullable=True),
    sa.Column('description_ru', sa.Text(), nullable=True),
    sa.Column('description_ua', sa.Text(), nullable=True),
    sa.Column('description_tr', sa.Text(), nullable=True),
    sa.Column('is_available', sa.Boolean(), nullable=True),
    sa.Column('code', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_categories_id'), 'categories', ['id'], unique=False)
    op.create_table('colors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('value', sa.String(), nullable=False),
    sa.Column('code', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_colors_id'), 'colors', ['id'], unique=False)
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('order_status', sa.String(), nullable=False),
    sa.Column('country', sa.String(), nullable=True),
    sa.Column('city', sa.String(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('delivery_method', sa.String(), nullable=False),
    sa.Column('payment_method', sa.String(), nullable=False),
    sa.Column('total_price', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_orders_id'), 'orders', ['id'], unique=False)
    op.create_table('sizes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('value', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sizes_id'), 'sizes', ['id'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('registered_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title_en', sa.String(), nullable=False),
    sa.Column('title_ru', sa.String(), nullable=True),
    sa.Column('title_ua', sa.String(), nullable=True),
    sa.Column('title_tr', sa.String(), nullable=True),
    sa.Column('is_available', sa.Boolean(), nullable=True),
    sa.Column('code', sa.String(), nullable=True),
    sa.Column('description_en', sa.Text(), nullable=True),
    sa.Column('description_ru', sa.Text(), nullable=True),
    sa.Column('description_ua', sa.Text(), nullable=True),
    sa.Column('description_tr', sa.Text(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('sale', sa.Boolean(), nullable=True),
    sa.Column('discount_value', sa.Integer(), nullable=True),
    sa.Column('avatar', sa.String(), nullable=True),
    sa.Column('slides', sa.String(), nullable=True),
    sa.Column('video', sa.String(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_products_id'), 'products', ['id'], unique=False)
    op.create_table('types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('size_id', sa.Integer(), nullable=True),
    sa.Column('color_id', sa.Integer(), nullable=True),
    sa.Column('is_available', sa.Boolean(), nullable=True),
    sa.Column('remainder', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.String(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['color_id'], ['colors.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['size_id'], ['sizes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_types_id'), 'types', ['id'], unique=False)
    op.create_table('order_items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('type_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('price_per_unit', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['type_id'], ['types.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_order_items_id'), 'order_items', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_order_items_id'), table_name='order_items')
    op.drop_table('order_items')
    op.drop_index(op.f('ix_types_id'), table_name='types')
    op.drop_table('types')
    op.drop_index(op.f('ix_products_id'), table_name='products')
    op.drop_table('products')
    op.drop_table('user')
    op.drop_index(op.f('ix_sizes_id'), table_name='sizes')
    op.drop_table('sizes')
    op.drop_index(op.f('ix_orders_id'), table_name='orders')
    op.drop_table('orders')
    op.drop_index(op.f('ix_colors_id'), table_name='colors')
    op.drop_table('colors')
    op.drop_index(op.f('ix_categories_id'), table_name='categories')
    op.drop_table('categories')
    # ### end Alembic commands ###