"""fix service catalog

Revision ID: 09c9c49980b5
Revises: 14340bc48a0d
Create Date: 2026-09-30 06:49:45.889419

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '09c9c49980b5'
down_revision: Union[str, Sequence[str], None] = '14340bc48a0d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
