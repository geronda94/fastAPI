"""Fix migrations after product_sizes drop

Revision ID: 55fdb08896f2
Revises: 7920755b2195
Create Date: 2024-12-07 20:03:36.108794

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '55fdb08896f2'
down_revision: Union[str, None] = '7920755b2195'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_stocks_id', table_name='stocks')
    op.drop_table('stocks')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stocks',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('product_color_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('size_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('quantity', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['product_color_id'], ['product_colors.id'], name='stocks_product_color_id_fkey'),
    sa.ForeignKeyConstraint(['size_id'], ['sizes.id'], name='stocks_size_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='stocks_pkey')
    )
    op.create_index('ix_stocks_id', 'stocks', ['id'], unique=False)
    # ### end Alembic commands ###
