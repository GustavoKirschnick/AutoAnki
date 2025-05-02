from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_session
from app.models import PromptModifierDB
from app.schemas import (
    Message,
    PromptModifier,
    PromptModifierList,
    PromptModifierPublic,
    PromptModifierUpdate,
)

prompt_modifiers_router = APIRouter(prefix='/prompt-modifiers', tags=['Prompt Modifiers'])


@prompt_modifiers_router.post('/', status_code=HTTPStatus.CREATED, response_model=PromptModifierPublic)
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


@prompt_modifiers_router.delete('/{prompt_modifier_id}', response_model=Message)
def delete_prompt_modifier(prompt_modifier_id: int, session: Session = Depends(get_session)):
    db_prompt_modifier = session.scalar(select(PromptModifierDB).where(PromptModifierDB.id == prompt_modifier_id))

    if not db_prompt_modifier:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=f'Prompt modifier with id {prompt_modifier_id} not found'
        )

    session.delete(db_prompt_modifier)
    session.commit()

    return {'message': 'Prompt modifier deleted'}


@prompt_modifiers_router.get('/', response_model=PromptModifierList)
def get_prompt_modifiers(limit: int = 10, session: Session = Depends(get_session)):
    prompt_modifiers = session.scalars(select(PromptModifierDB).limit(limit))

    return {'prompt_modifiers': prompt_modifiers}


@prompt_modifiers_router.get('/{prompt_modifier_id}', response_model=PromptModifierPublic)
def get_prompt_by_id(prompt_modifier_id: int, session: Session = Depends(get_session)):
    prompt_modifier = session.scalar(select(PromptModifierDB).where(PromptModifierDB.id == prompt_modifier_id))

    if not prompt_modifier:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=f'Prompt modifier with id {prompt_modifier_id} not found'
        )

    return prompt_modifier


@prompt_modifiers_router.put('/{prompt_modifier_id}', status_code=HTTPStatus.OK, response_model=Message)
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
