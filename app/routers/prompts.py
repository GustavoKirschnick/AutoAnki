from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_session
from app.models import PromptDB
from app.schemas import (
    Message,
    PromptList,
    Prompts,
    PromptsPublic,
    PromptUpdate,
)

prompts_router = APIRouter(prefix='/prompts', tags=['Prompts'])


@prompts_router.post('/', status_code=HTTPStatus.CREATED, response_model=PromptsPublic)
def create_prompt(prompt: Prompts, session: Session = Depends(get_session)):
    db_prompt = session.scalar(select(PromptDB).where(PromptDB.name == prompt.name))

    if db_prompt:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'There is already a prompt with the name of {db_prompt.name}',
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
def update_prompt_by_id(
    prompt_id: int, update_data: PromptUpdate, session: Session = Depends(get_session)
):
    prompt = session.scalar(select(PromptDB).where(PromptDB.id == prompt_id))

    if not prompt:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=f'Prompt with id {prompt_id} not found'
        )

    prompt.name = update_data.name
    prompt.prompt = update_data.prompt
    session.commit()
    session.refresh(prompt)

    return {'message': 'The prompt was updated'}
