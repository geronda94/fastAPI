"""Fix foreign key in order_items

Revision ID: 8e164ffb2086
Revises: 9b6175ef29a6
Create Date: 2024-11-18 22:09:58.121062

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8e164ffb2086'
down_revision: Union[str, None] = '9b6175ef29a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
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
    op.create_table('user_strlete',
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
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_products_id'), 'products', ['id'], unique=False)
    op.create_table('product_colors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('color_id', sa.Integer(), nullable=False),
    sa.Column('avatar', sa.String(), nullable=True),
    sa.Column('slides', sa.String(), nullable=True),
    sa.Column('video', sa.String(), nullable=True),
    sa.Column('is_available', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['color_id'], ['colors.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_product_colors_id'), 'product_colors', ['id'], unique=False)
    op.create_table('product_sizes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_color_id', sa.Integer(), nullable=False),
    sa.Column('size_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_color_id'], ['product_colors.id'], ),
    sa.ForeignKeyConstraint(['size_id'], ['sizes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_product_sizes_id'), 'product_sizes', ['id'], unique=False)
    op.create_table('order_items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('product_color_id', sa.Integer(), nullable=True),
    sa.Column('product_syze_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('price_per_unit', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.ForeignKeyConstraint(['product_color_id'], ['product_colors.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['product_syze_id'], ['product_sizes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_order_items_id'), 'order_items', ['id'], unique=False)
    op.add_column('colors', sa.Column('name', sa.String(), nullable=False))
    op.drop_column('colors', 'value')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('colors', sa.Column('value', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('colors', 'name')
    op.drop_index(op.f('ix_order_items_id'), table_name='order_items')
    op.drop_table('order_items')
    op.drop_index(op.f('ix_product_sizes_id'), table_name='product_sizes')
    op.drop_table('product_sizes')
    op.drop_index(op.f('ix_product_colors_id'), table_name='product_colors')
    op.drop_table('product_colors')
    op.drop_index(op.f('ix_products_id'), table_name='products')
    op.drop_table('products')
    op.drop_table('user_strlete')
    op.drop_index(op.f('ix_orders_id'), table_name='orders')
    op.drop_table('orders')
    # ### end Alembic commands ###
