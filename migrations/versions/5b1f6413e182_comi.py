"""comi

Revision ID: 5b1f6413e182
Revises: 2953df33df2b
Create Date: 2024-08-17 23:09:33.804639

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b1f6413e182'
down_revision: Union[str, None] = '2953df33df2b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('operation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.String(), nullable=True),
    sa.Column('figi', sa.String(), nullable=True),
    sa.Column('instrument_type', sa.String(), nullable=True),
    sa.Column('date', sa.TIMESTAMP(), nullable=True),
    sa.Column('type', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_constraint('user_email_key', 'user', type_='unique')
    op.drop_constraint('user_username_key', 'user', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('user_username_key', 'user', ['username'])
    op.create_unique_constraint('user_email_key', 'user', ['email'])
    op.drop_table('operation')
    # ### end Alembic commands ###