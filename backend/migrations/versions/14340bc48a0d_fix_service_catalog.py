"""fix service catalog

Revision ID: 14340bc48a0d
Revises: 6e6e3d11df9e
Create Date: 2026-09-30 12:19:24.756577

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14340bc48a0d'
down_revision: Union[str, Sequence[str], None] = '6e6e3d11df9e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
