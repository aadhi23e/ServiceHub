"""add service catalog

Revision ID: 62cc74e7cce2
Revises: 3481a60260c3
Create Date: 2026-09-30 12:01:46.736831

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '62cc74e7cce2'
down_revision: Union[str, Sequence[str], None] = '3481a60260c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
