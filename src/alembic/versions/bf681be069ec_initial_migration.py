"""Initial migration

Revision ID: bf681be069ec
Revises: 922d2f082dd7
Create Date: 2024-12-07 19:48:35.909640

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bf681be069ec'
down_revision: Union[str, None] = '922d2f082dd7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stocks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_color_id', sa.Integer(), nullable=False),
    sa.Column('size_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_color_id'], ['product_colors.id'], ),
    sa.ForeignKeyConstraint(['size_id'], ['sizes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_stocks_id'), 'stocks', ['id'], unique=False)
    op.drop_index('ix_product_sizes_id', table_name='product_sizes')
    op.drop_table('product_sizes')
    op.add_column('colors', sa.Column('sizes', sa.JSON(), nullable=True))
    op.drop_constraint('order_items_product_syze_id_fkey', 'order_items', type_='foreignkey')
    op.drop_column('order_items', 'product_syze_id')
    op.drop_column('orders', 'payment_method')
    op.drop_column('orders', 'delivery_method')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('delivery_method', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('orders', sa.Column('payment_method', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('order_items', sa.Column('product_syze_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('order_items_product_syze_id_fkey', 'order_items', 'product_sizes', ['product_syze_id'], ['id'])
    op.drop_column('colors', 'sizes')
    op.create_table('product_sizes',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('product_color_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('size_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('quantity', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['product_color_id'], ['product_colors.id'], name='product_sizes_product_color_id_fkey'),
    sa.ForeignKeyConstraint(['size_id'], ['sizes.id'], name='product_sizes_size_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='product_sizes_pkey')
    )
    op.create_index('ix_product_sizes_id', 'product_sizes', ['id'], unique=False)
    op.drop_index(op.f('ix_stocks_id'), table_name='stocks')
    op.drop_table('stocks')
    # ### end Alembic commands ###
