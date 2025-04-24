from pydantic import BaseModel


class CardOutput(BaseModel):
    words: str
    front: str
    back: str


class ExportAnki(BaseModel):
    cards: list[CardOutput]
    deck: str = None
    tag: str = None


class GenerateCardsInput(BaseModel):
    words: list[str]
    prompt: str
    modifier: list[str]


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


class PromptList(BaseModel):
    prompts: list[PromptsPublic]


class PromptModifierList(BaseModel):
    prompt_modifiers: list[PromptModifierPublic]
