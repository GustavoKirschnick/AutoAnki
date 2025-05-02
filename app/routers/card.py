from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.core.anki_export import AnkiExporter
from app.core.card import Card
from app.core.cards_generator import CardGenerator
from app.schemas import CardOutput, ExportAnki, GenerateCardsInput

card_router = APIRouter(tags=['Cards'])


@card_router.post('/generate-cards/', status_code=HTTPStatus.CREATED, response_model=list[CardOutput])
def generate_cards(payload: GenerateCardsInput):
    if not payload.words:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Empty word list'
        )

    card_generator = CardGenerator()
    cards: list[Card] = card_generator.generate_cards(payload.words, payload.prompt, payload.modifier)
    print(cards)
    return [
        CardOutput(
            word=card.word,
            front=card.front,
            back=card.back
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
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f'{e}')
