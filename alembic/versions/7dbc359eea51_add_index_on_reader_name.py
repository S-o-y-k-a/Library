"""add index on reader name

Revision ID: 7dbc359eea51
Revises: 3f6960efd7db
Create Date: 2025-12-28 23:19:21.364985

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7dbc359eea51'
down_revision: Union[str, Sequence[str], None] = '3f6960efd7db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
   op.create_index('ix_reader_name', 'reader', ['name'])


def downgrade():
    op.drop_index('ix_reader_name', table_name='reader')
