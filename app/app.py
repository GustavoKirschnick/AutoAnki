from fastapi import FastAPI

from app.routers.card import card_router
from app.routers.prompt_modifiers import prompt_modifiers_router
from app.routers.prompts import prompts_router

app = FastAPI()

app.include_router(card_router)
app.include_router(prompts_router)
app.include_router(prompt_modifiers_router)
