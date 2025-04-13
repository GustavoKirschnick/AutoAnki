from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_session
from app.models import WordDB, CardDB, PromptDB, PromptModifierDB
from app.schemas import Cards, CardPublic, Message, Word, WordList, WordPublic, CardList, Prompts, PromptsPublic, PromptList

app = FastAPI()


@app.post('/words/', status_code=HTTPStatus.CREATED, response_model=WordPublic)
def create_word(word: Word, session=Depends(get_session)):
    db_word = session.scalar(select(WordDB).where(WordDB.word == word.word))

    if db_word:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='The word is already registered in other cards',
        )

    db_word = WordDB(word=word.word, type=word.type)
    session.add(db_word)
    session.commit()
    session.refresh(db_word)

    return db_word


@app.get('/words/', response_model=WordList)
def show_words(limit: int = 10, session: Session = Depends(get_session)):
    words = session.scalars(select(WordDB).limit(limit))

    if not words:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail = 'There are no words to be shown'
        )

    return {'words': words}


@app.delete('/words/{word_id}', response_model=Message)
def delete_word(word_id: int, session: Session = Depends(get_session)):
    db_word = session.scalar(select(WordDB).where(WordDB.id == word_id))

    if not db_word:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Word not found'
        )

    session.delete(db_word)
    session.commit()

    return {'message': 'Word deleted'}


# Rota temp. para testar banco de dados:

@app.post('/cards/', status_code=HTTPStatus.CREATED, response_model=CardPublic)
def create_card(card: Cards, session=Depends(get_session)):
    db_card = session.scalar(select(CardDB).where(CardDB.front_card == card.front_card or CardDB.back_card == card.back_card))

    if db_card:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail= 'The card already exists'
        )
    
    db_word = session.scalars(select(WordDB).where(WordDB.word.in_(card.reference_word))).all()
    if not db_word:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="At least one reference word must exist"
        )
    
    db_prompt = session.scalar(select(PromptDB).where(PromptDB.id == card.prompt_id))
  
    if not db_prompt:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail = 'No prompt found matching the id'
        )
    
    db_prompt_modifiers = session.scalars(select(PromptModifierDB).where(PromptModifierDB.id.in_(card.prompt_modifier))).all()

    db_card = CardDB(
    front_card=card.front_card, 
    back_card=card.back_card, 
    prompt=db_prompt,
    reference_words=db_word,
    prompt_modifiers=db_prompt_modifiers
    )

    session.add(db_card)
    session.commit()
    session.refresh(db_card)

    return db_card

@app.delete('/cards/{card_id}', response_model=Message)
def delete_card(card_id: int, session: Session = Depends(get_session)):
    db_card = session.scalar(select(CardDB).where(CardDB.id == card_id))

    if not db_card:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Card not found'
        )
    
    session.delete(db_card)
    session.commit()

    return {'message': 'Card deleted'}

@app.get('/cards/', response_model=CardList)
def show_cards(limit: int = 10, session: Session = Depends(get_session)):
    cards = session.scalars(select(CardDB).limit(limit))
    
    # This does not work:
    if not cards:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail = 'There are no cards to be shown'
        )
    
    return {'cards': cards}

@app.post('/prompts/', status_code=HTTPStatus.CREATED, response_model = PromptsPublic)
def create_prompt(prompt: Prompts , session: Session = Depends(get_session)):
    db_prompt = session.scalar(select(PromptDB).where(PromptDB.name == prompt.name))

    if db_prompt:
        raise HTTPException(
            detail=f'There is already a prompt with the name of {db_prompt.name}'
        )
    
    db_prompt = PromptDB(name=prompt.name, prompt=prompt.prompt)
    session.add(db_prompt)
    session.commit()
    session.refresh(db_prompt)

    return db_prompt

@app.delete('/prompts/{prompt_id}', response_model=Message)
def delete_prompt(prompt_id: int, session: Session = Depends(get_session)):
    db_prompt = session.scalar(select(PromptDB).where(PromptDB.id == prompt_id))

    if not db_prompt:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Prompt not found'
        )
    
    session.delete(db_prompt)
    session.commit()

    return {'message': 'Prompt deleted'}

@app.get('/prompts/',response_model = PromptList)
def get_prompts(limit: int = 10, session: Session = Depends(get_session)):
    prompts = session.scalars(select(PromptDB).limit(limit))

    return {'prompts': prompts}

@app.get('/prompts/{prompt_id}', response_model= PromptsPublic)
def get_prompt_by_id(prompt_id: int, session: Session = Depends(get_session)):
    prompt = session.scalar(select(PromptDB).where(PromptDB.id == prompt_id))

    if not prompt:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail= 'Prompt with id not found'
        )
    
    return {'prompt': prompt}
