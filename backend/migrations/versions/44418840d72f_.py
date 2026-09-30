"""empty message

Revision ID: 44418840d72f
Revises: 09c9c49980b5
Create Date: 2026-09-30 06:52:17.185416

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '44418840d72f'
down_revision: Union[str, Sequence[str], None] = '09c9c49980b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
