"""Initial migration

Revision ID: 231329826d7a
Revises: cace6f37b362
Create Date: 2024-12-07 13:55:41.505790

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '231329826d7a'
down_revision: Union[str, None] = 'cace6f37b362'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('categories', 'title_tr')
    op.drop_column('categories', 'description_tr')
    op.drop_column('product_colors', 'video')
    op.add_column('products', sa.Column('id_crm', sa.String(), nullable=True))
    op.alter_column('products', 'title_en',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('products', 'title_ua',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_column('products', 'title_tr')
    op.drop_column('products', 'description_tr')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('description_tr', sa.TEXT(), autoincrement=False, nullable=True))
    op.add_column('products', sa.Column('title_tr', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.alter_column('products', 'title_ua',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('products', 'title_en',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_column('products', 'id_crm')
    op.add_column('product_colors', sa.Column('video', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('categories', sa.Column('description_tr', sa.TEXT(), autoincrement=False, nullable=True))
    op.add_column('categories', sa.Column('title_tr', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###