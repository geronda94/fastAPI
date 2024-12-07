"""Initial migration

Revision ID: 922d2f082dd7
Revises: 231329826d7a
Create Date: 2024-12-07 14:11:40.037361

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '922d2f082dd7'
down_revision: Union[str, None] = '231329826d7a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'video')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('video', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###