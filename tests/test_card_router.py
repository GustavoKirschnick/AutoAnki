from http import HTTPStatus
from pathlib import Path

from app.core.card import Card


def test_create_valid_card(monkeypatch, client):

    def mock_generate_cards(self, words, prompt, modifiers):
        return [Card(word=w, front=f'Front of {w}', back=f'Back of {w}') for w in words]

    monkeypatch.setattr('app.routers.card.CardGenerator.generate_cards', mock_generate_cards)

    payload = {'words': ['Beobachten'], 'prompt': 'Create a sentence', 'modifier': ['Use the Konjuntiv 2']}

    response = client.post('/generate-cards/', json=payload)

    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert len(data) == 1
    assert data[0]['word'] == "Beobachten"
    assert data[0]['front'] == "Front of Beobachten"
    assert data[0]['back'] == "Back of Beobachten"


def test_create_invalid_card(client):
    payload = {'words': [], 'prompt': 'Create a sentence', 'modifier': ['Use the Konjuntiv 2']}

    create_response = client.post('/generate-cards/', json=payload)
    assert create_response.status_code == HTTPStatus.BAD_REQUEST
    assert create_response.json()['detail'] == 'Empty word list'


def test_export_valid_card(monkeypatch, client):
    dummy_file_path = 'exports/test_deck_20250430120000.apkg'

    class MockAnkiExporter:
        def __init__(self, deck_name, tag, output_dir='exports'):
            self.deck_name = deck_name
            self.tag = tag
            self.output_dir = output_dir

        def create_cards(self, cards):
            pass

        def export(self):
            Path(self.output_dir).mkdir(parents=True, exist_ok=True)
            Path(dummy_file_path).write_text('Fake .apkg content')
            return dummy_file_path

    monkeypatch.setattr('app.routers.card.AnkiExporter', MockAnkiExporter)

    payload = {
        'deck': 'Test Deck',
        'tag': 'test_tag',
        'cards': [
            {'word': 'Beobachten', 'front': 'Front of Beobachten', 'back': 'Back of Beobachten'}
        ]
    }

    response = client.post('/export-cards/', json=payload)

    assert response.status_code == HTTPStatus.OK
    assert response.headers['content-type'] == 'application/apkg'
    assert response.headers['content-disposition'].endswith('.apkg"')

    # Deletes the test file
    Path(dummy_file_path).unlink()


def test_export_invalid_payload(client):
    invalid_payload = {
        'deck': 'DeckName',
        'tag': 'TagDeck',
        'cards': [
            {'word': 'Beobachten', 'front': 'Er wird beobachtet'}
        ]
    }

    response = client.post('/export-cards/', json=invalid_payload)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_export_cards_internal_error(monkeypatch, client):
    class MockAnkiExporter:
        def __init__(self, deck_name, tag, output_dir='exports'):
            self.deck_name = deck_name
            self.tag = tag
            self.output_dir = output_dir

        def create_cards(self, cards):
            pass

        def export(self):
            raise Exception('Simulated error in the exporting')

    monkeypatch.setattr('app.routers.card.AnkiExporter', MockAnkiExporter)

    payload = {
        'deck': 'TestDeck',
        'tag': 'TestTag',
        'cards': [{'word': 'Beobachten', 'front': 'Er wird beobachtet', 'back': 'He is being watched'}]
    }

    response = client.post('/export-cards/', json=payload)

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json()['detail'] == 'Simulated error in the exporting'
