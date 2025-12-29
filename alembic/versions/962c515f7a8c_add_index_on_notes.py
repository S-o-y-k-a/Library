"""add index on notes

Revision ID: 962c515f7a8c
Revises: 666aa926b968
Create Date: 2025-12-29 20:22:03.320341

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '962c515f7a8c'
down_revision: Union[str, Sequence[str], None] = '666aa926b968'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
    op.create_index("idx_gin","issuance", ["notes"], postgresql_using="gin")
    op.execute("CREATE INDEX idx_pg_trgm ON issuance USING gin ((notes::text) gin_trgm_ops);")
    pass


def downgrade() -> None:
    op.drop_index('idx_gin', table_name='issuance')
    op.execute("DROP INDEX idx_pg_trgm")
    pass
