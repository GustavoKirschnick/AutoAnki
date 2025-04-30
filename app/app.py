from http import HTTPStatus

from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.anki_export import AnkiExporter
from app.card import Card
from app.cards_generator import CardGenerator
from app.database import get_session
from app.models import PromptDB, PromptModifierDB
from app.schemas import (
    CardOutput,
    ExportAnki,
    GenerateCardsInput,
    Message,
    PromptList,
    PromptModifier,
    PromptModifierList,
    PromptModifierPublic,
    PromptModifierUpdate,
    Prompts,
    PromptsPublic,
    PromptUpdate,
)

app = FastAPI()


prompts_router = APIRouter(prefix='/prompts', tags=['Prompts'])


@prompts_router.post('/', status_code=HTTPStatus.CREATED, response_model=PromptsPublic)
def create_prompt(prompt: Prompts, session: Session = Depends(get_session)):
    db_prompt = session.scalar(select(PromptDB).where(PromptDB.name == prompt.name))

    if db_prompt:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=f'There is already a prompt with the name of {db_prompt.name}'
        )

    db_prompt = PromptDB(name=prompt.name, prompt=prompt.prompt)
    session.add(db_prompt)
    session.commit()
    session.refresh(db_prompt)

    return db_prompt


@prompts_router.delete('/{prompt_id}', response_model=Message)
def delete_prompt(prompt_id: int, session: Session = Depends(get_session)):
    db_prompt = session.scalar(select(PromptDB).where(PromptDB.id == prompt_id))

    if not db_prompt:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=f'Prompt with id {prompt_id} not found'
        )

    session.delete(db_prompt)
    session.commit()

    return {'message': 'Prompt deleted'}


@prompts_router.get('/', response_model=PromptList)
def get_prompts(limit: int = 10, session: Session = Depends(get_session)):
    prompts = session.scalars(select(PromptDB).limit(limit))

    return {'prompts': prompts}


@prompts_router.get('/{prompt_id}', response_model=PromptsPublic)
def get_prompt_by_id(prompt_id: int, session: Session = Depends(get_session)):
    prompt = session.scalar(select(PromptDB).where(PromptDB.id == prompt_id))
    if not prompt:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=f'Prompt with id {prompt_id} not found'
        )

    return prompt


@prompts_router.put('/{prompt_id}', status_code=HTTPStatus.OK, response_model=Message)
def update_prompt_by_id(prompt_id: int, update_data: PromptUpdate, session: Session = Depends(get_session)):
    prompt = session.scalar(select(PromptDB).where(PromptDB.id == prompt_id))

    if not prompt:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Prompt with id {prompt_id} not found'
        )

    prompt.name = update_data.name
    prompt.prompt = update_data.prompt
    session.commit()
    session.refresh(prompt)

    return {'message': 'The prompt was updated'}


prompt_modifier_router = APIRouter(prefix='/prompt-modifiers', tags=['Prompt Modifiers'])


@prompt_modifier_router.post('/', status_code=HTTPStatus.CREATED, response_model=PromptModifierPublic)
def create_prompt_modifier(prompt_modifier: PromptModifier, session: Session = Depends(get_session)):
    db_prompt_modifier = session.scalar(select(PromptModifierDB).where(PromptModifierDB.name == prompt_modifier.name))

    if db_prompt_modifier:
        raise HTTPException(
             status_code=HTTPStatus.BAD_REQUEST, detail=f'There is already a prompt modifier with the name of {db_prompt_modifier.name}'
        )

    db_prompt_modifier = PromptModifierDB(name=prompt_modifier.name, prompt=prompt_modifier.prompt)
    session.add(db_prompt_modifier)
    session.commit()
    session.refresh(db_prompt_modifier)

    return db_prompt_modifier


@prompt_modifier_router.delete('/{prompt_modifier_id}', response_model=Message)
def delete_prompt_modifier(prompt_modifier_id: int, session: Session = Depends(get_session)):
    db_prompt_modifier = session.scalar(select(PromptModifierDB).where(PromptModifierDB.id == prompt_modifier_id))

    if not db_prompt_modifier:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=f'Prompt modifier with id {prompt_modifier_id} not found'
        )

    session.delete(db_prompt_modifier)
    session.commit()

    return {'message': 'Prompt modifier deleted'}


@prompt_modifier_router.get('/', response_model=PromptModifierList)
def get_prompt_modifiers(limit: int = 10, session: Session = Depends(get_session)):
    prompt_modifiers = session.scalars(select(PromptModifierDB).limit(limit))

    return {'prompt_modifiers': prompt_modifiers}


@prompt_modifier_router.get('/{prompt_modifier_id}', response_model=PromptModifierPublic)
def get_prompt_by_id(prompt_modifier_id: int, session: Session = Depends(get_session)):
    prompt_modifier = session.scalar(select(PromptModifierDB).where(PromptModifierDB.id == prompt_modifier_id))

    if not prompt_modifier:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=f'Prompt modifier with id {prompt_modifier_id} not found'
        )

    return prompt_modifier


@prompt_modifier_router.put('/{prompt_modifier_id}', status_code=HTTPStatus.OK, response_model=Message)
def update_prompt_by_id(prompt_modifier_id: int, update_data: PromptModifierUpdate, session: Session = Depends(get_session)):
    prompt_modifier = session.scalar(select(PromptModifierDB).where(PromptModifierDB.id == prompt_modifier_id))

    if not prompt_modifier:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Prompt modifier with id {prompt_modifier_id} not found'
        )

    prompt_modifier.name = update_data.name
    prompt_modifier.prompt = update_data.prompt
    session.commit()
    session.refresh(prompt_modifier)

    return {'message': 'The prompt modifier was updated'}


card_router = APIRouter(tags=['Cards'])


@card_router.post('/generate-cards/', status_code=HTTPStatus.CREATED, response_model=list[CardOutput])
def generate_cards(payload: GenerateCardsInput):
    if not payload.words:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Empty word list'
        )

    card_generator = CardGenerator()
    cards: list[Card] =  card_generator.generate_cards(payload.words, payload.prompt, payload.modifier)
    print(cards)
    return [
        CardOutput(
            word = card.word,
            front = card.front,
            back = card.back
        )
        for card in cards
    ]


@card_router.post('/export-cards/')
def export_cards_to_anki(cards: ExportAnki):
    try:
        anki_exporter = AnkiExporter(
            deck_name=cards.deck,
            tag=cards.tag,      
        )

        card_data = [{'front': card.front, 'back': card.back} for card in cards.cards]
        anki_exporter.create_cards(card_data)
        path = anki_exporter.export()

        return FileResponse(path, media_type='application/apkg', filename=path.split('/')[-1])
    
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail= f'{e}')

app.include_router(prompts_router)
app.include_router(prompt_modifier_router)
app.include_router(card_router)
