"""Adjust database structure

Revision ID: 7813027d564d
Revises: 
Create Date: 2023-10-05 19:53:55.347863

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7813027d564d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('steamid_data',
    sa.Column('steamid', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('buildid', sa.String(), nullable=False),
    sa.Column('serverid', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('steamid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('steamid_data')
    # ### end Alembic commands ###