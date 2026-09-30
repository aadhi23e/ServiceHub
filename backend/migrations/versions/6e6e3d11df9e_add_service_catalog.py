"""add service catalog

Revision ID: 6e6e3d11df9e
Revises: 62cc74e7cce2
Create Date: 2026-09-30 06:34:27.525921

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e6e3d11df9e'
down_revision: Union[str, Sequence[str], None] = '62cc74e7cce2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
