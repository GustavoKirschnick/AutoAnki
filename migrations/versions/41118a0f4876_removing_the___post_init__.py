"""Removing the  __post_init__

Revision ID: 41118a0f4876
Revises: 6cd24bb466a0
Create Date: 2025-04-07 18:33:09.845513

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '41118a0f4876'
down_revision: Union[str, None] = '6cd24bb466a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
