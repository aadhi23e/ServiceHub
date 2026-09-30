"""empty message

Revision ID: 3c970ba5897f
Revises: 44418840d72f
Create Date: 2026-09-30 06:53:25.079943

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c970ba5897f'
down_revision: Union[str, Sequence[str], None] = '44418840d72f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
