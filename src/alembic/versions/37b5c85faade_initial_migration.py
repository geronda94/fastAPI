"""Initial migration

Revision ID: 37b5c85faade
Revises: 64c9da794915
Create Date: 2024-10-07 15:23:42.187414

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37b5c85faade'
down_revision: Union[str, None] = '64c9da794915'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sites', sa.Column('True', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sites', 'True')
    # ### end Alembic commands ###
