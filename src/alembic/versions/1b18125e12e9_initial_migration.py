"""Initial migration

Revision ID: 1b18125e12e9
Revises: 94cd79c63a51
Create Date: 2025-02-03 19:53:05.297164

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b18125e12e9'
down_revision: Union[str, None] = '94cd79c63a51'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('size_chart',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.Text(), nullable=False),
    sa.Column('table', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_size_chart_id'), 'size_chart', ['id'], unique=False)
    op.add_column('products', sa.Column('size_chart_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'products', 'size_chart', ['size_chart_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'products', type_='foreignkey')
    op.drop_column('products', 'size_chart_id')
    op.drop_index(op.f('ix_size_chart_id'), table_name='size_chart')
    op.drop_table('size_chart')
    # ### end Alembic commands ###
