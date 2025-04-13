"""Making reference_words and prompt_id mandatory paramethers

Revision ID: 30dec44622fd
Revises: 00e02f7ed6c4
Create Date: 2025-04-07 18:05:39.320738

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '30dec44622fd'
down_revision: Union[str, None] = '00e02f7ed6c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'cards_new',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('front_card', sa.String(), nullable=False),
        sa.Column('back_card', sa.String(), nullable=False),
        sa.Column('prompt_id', sa.Integer(), nullable=False),  # Agora 'prompt_id' é obrigatório
        sa.Column('reference_words', sa.String(), nullable=False),  # 'reference_words' obrigatório
        sa.ForeignKeyConstraint(['prompt_id'], ['prompts.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # Deletar a tabela antiga 'cards'
    op.drop_table('cards')

    # Renomear a nova tabela 'cards_new' para 'cards'
    op.rename_table('cards_new', 'cards')


def downgrade() -> None:
    op.create_table(
        'cards',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('front_card', sa.String(), nullable=False),
        sa.Column('back_card', sa.String(), nullable=False),
        sa.Column('prompt_id', sa.Integer(), nullable=True),  # 'prompt_id' não obrigatório
        sa.Column('reference_words', sa.String(), nullable=True),  # 'reference_words' não obrigatório
        sa.ForeignKeyConstraint(['prompt_id'], ['prompts.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # Deletar a nova tabela 'cards_new' se necessário
    op.drop_table('cards_new')
