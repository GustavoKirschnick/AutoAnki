"""Renaming card table to cards

Revision ID: 20e08123a6eb
Revises: ca37aa49e55b
Create Date: 2025-03-24 20:20:25.141741

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20e08123a6eb'
down_revision: Union[str, None] = 'ca37aa49e55b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'cards_temp',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('front_card', sa.String, nullable=False),
        sa.Column('back_card', sa.String, nullable=False),
        sa.Column('reference_word_id', sa.Integer, sa.ForeignKey('words.id'), nullable=False)
    )

    # Passo 2: Copiar os dados da tabela antiga para a tabela nova
    op.execute('INSERT INTO cards_temp (id, front_card, back_card, reference_word_id) SELECT id, front_card, back_card, reference_word_id FROM cards')

    # Passo 3: Excluir a tabela antiga
    op.drop_table('cards')

    # Passo 4: Renomear a tabela nova para 'cards'
    op.rename_table('cards_temp', 'cards')


def downgrade() -> None:
    op.create_table(
        'cards_temp',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('front_card', sa.String, nullable=False),
        sa.Column('back_card', sa.String, nullable=False),
        sa.Column('reference_word_id', sa.Integer, nullable=False)
    )

    # Passo 2: Copiar os dados da tabela atual para a tabela nova
    op.execute('INSERT INTO cards_temp (id, front_card, back_card, reference_word_id) SELECT id, front_card, back_card, reference_word_id FROM cards')

    # Passo 3: Excluir a tabela atual
    op.drop_table('cards')

    # Passo 4: Renomear a tabela temporária para 'cards'
    op.rename_table('cards_temp', 'cards')
