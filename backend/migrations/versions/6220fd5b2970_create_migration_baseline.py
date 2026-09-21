"""create migration baseline

Revision ID: 6220fd5b2970
Revises: 06e2829d5028
Create Date: 2026-09-19 10:41:51.106096

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6220fd5b2970'
down_revision: Union[str, Sequence[str], None] = '06e2829d5028'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
