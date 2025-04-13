from pydantic import BaseModel


class Word(BaseModel):
    word: str
    type: str


class CardPublic(BaseModel):
    id: int
    front_card: str
    back_card: str
    reference_word: list[str]
    prompt_id: int
    prompt_modifier: list[int]


class Cards(BaseModel):
    front_card: str
    back_card: str
    reference_word: list[str]
    prompt_id: int
    prompt_modifier: list[int]


class WordPublic(BaseModel):
    id: int
    word: str
    type: str
    cards: list[int]


class Prompts(BaseModel):
    name: str
    prompt: str


class PromptsPublic(BaseModel):
    id: int
    name: str
    prompt: str

    class Config:
        orm_mode = True 


class PromptUpdate(BaseModel):
    name: str
    prompt: str


class PromptModifier(BaseModel):
    name: str
    prompt: str


class PromptModifierPublic(BaseModel):
    id: int
    name: str
    prompt: str


class PromptModifierUpdate(BaseModel):
    name: str
    prompt: str


class Message(BaseModel):
    message: str


class WordList(BaseModel):
    words: list[WordPublic]


class CardList(BaseModel):
    cards: list[CardPublic]


class PromptList(BaseModel):
    prompts: list[PromptsPublic]


class PromptModifierList(BaseModel):
    prompt_modifiers: list[PromptModifierPublic]
