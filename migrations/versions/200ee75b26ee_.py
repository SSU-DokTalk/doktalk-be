"""empty message

Revision ID: 200ee75b26ee
Revises: 8fadad27cf58
Create Date: 2024-11-13 22:12:13.200933

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '200ee75b26ee'
down_revision: Union[str, None] = '8fadad27cf58'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('oauth', 'createdAt',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               nullable=False)
    op.alter_column('user', 'createdAt',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_nullable=False)
    op.alter_column('user', 'updatedAt',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('now()'),
               existing_nullable=False)
    op.alter_column('user', 'isDeleted',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'isDeleted',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=True)
    op.alter_column('user', 'updatedAt',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_nullable=False)
    op.alter_column('user', 'createdAt',
               existing_type=mysql.DATETIME(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_nullable=False)
    op.alter_column('oauth', 'createdAt',
               existing_type=mysql.DATETIME(),
               server_default=None,
               nullable=True)
    # ### end Alembic commands ###
