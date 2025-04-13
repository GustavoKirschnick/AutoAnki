"""Adding the created_at columns to CardDB

Revision ID: 6cd24bb466a0
Revises: 30dec44622fd
Create Date: 2025-04-07 18:14:41.752752

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6cd24bb466a0'
down_revision: Union[str, None] = '30dec44622fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('cards', sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()))
    


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('cards', 'created_at')
