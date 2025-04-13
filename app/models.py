# ruff: noqa
from datetime import datetime

from sqlalchemy import ForeignKey, func, Table, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()

card_words = Table(
    'card_words',
    table_registry.metadata,
    Column("card_id", Integer, ForeignKey("cards.id"), primary_key=True),
    Column("word_id", Integer, ForeignKey("words.id"), primary_key=True),
)

card_prompt_modifiers = Table(
    'card_prompt_modifiers',
    table_registry.metadata,
    Column("card_id", Integer, ForeignKey("cards.id"), primary_key=True),
    Column("modifier_id", Integer, ForeignKey("prompt_modifiers.id"), primary_key=True),
)

@table_registry.mapped_as_dataclass
class WordDB:
    __tablename__ = 'words'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    word: Mapped[str] = mapped_column(unique=True)
    type: Mapped[str] = mapped_column(nullable=False)

    cards: Mapped[list['CardDB']] = relationship(
        secondary= card_words, 
        back_populates='reference_words',
        init = False
        )

@table_registry.mapped_as_dataclass
class PromptDB:
    __tablename__ = 'prompts'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    prompt: Mapped[str] = mapped_column(nullable=False)

    cards: Mapped[list['CardDB']] = relationship(
        back_populates='prompt', 
        cascade= 'all, delete-orphan', 
        init = False
        )

    is_created_by_user: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())

@table_registry.mapped_as_dataclass
class PromptModifierDB:
    __tablename__ = 'prompt_modifiers'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    prompt: Mapped[str] = mapped_column(nullable=False)

    cards: Mapped[list['CardDB']] = relationship(
        secondary= card_prompt_modifiers,
        back_populates= 'prompt_modifiers',
        init = False
    )

    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    is_created_by_user: Mapped[bool] = mapped_column(default=False)

@table_registry.mapped_as_dataclass
class CardDB:
    __tablename__ = 'cards'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    front_card: Mapped[str] = mapped_column()
    back_card: Mapped[str] = mapped_column()
 
    reference_words: Mapped[list['WordDB']] = relationship(
        secondary=card_words,
        back_populates= 'cards',
        init = False
    )

    prompt_id : Mapped[int] = mapped_column(ForeignKey('prompts.id'), nullable=False)
    prompt: Mapped['PromptDB'] = relationship(
        back_populates='cards',
        init = False
        )

    prompt_modifiers: Mapped[list['PromptModifierDB']] = relationship(
        secondary= card_prompt_modifiers,
        back_populates= 'cards',
        init = False
    )
    
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )