import os
import random
from datetime import datetime

import genanki


class AnkiExporter:
    def __init__(self, deck_name: str = 'Default Deck', tag: str = None, output_dir: str = 'exports'):
        self.deck_name = deck_name
        self.tag = tag
        self.output_dir = output_dir
        self.model_id = random.randrange(1 << 30, 1 << 31)
        self.deck_id = random.randrange(1 << 30, 1 << 31)
        self.model = self._create_model()
        self.deck = self._create_deck()

    def _create_model(self):
        """Creates the Anki card model"""
        return genanki.Model(
            self.model_id,
            'Simple Model',
            fields=[
                {'name': 'Front'},
                {'name': 'Back'},
            ],
            templates=[
                {
                    'name': 'Card 1',
                    'qfmt': '{{Front}}',
                    'afmt': '{{Front}}<hr id="answer">{{Back}}',
                },
            ]
        )

    def _create_deck(self):
        """Creates the Anki deck with a given name"""
        return genanki.Deck(self.deck_id, self.deck_name)

    def create_card(self, front: str, back: str):
        """Creates a card in the deck"""
        note = genanki.Note(
            model=self.model,
            fields=[front, back],
            tags=[self.tag] if self.tag else []
        )

        self.deck.add_note(note)

    def create_cards(self, cards: list[dict]):
        """Creates multiple cards"""
        for card in cards:
            self.create_card(card['front'], card['back'])

    def export(self):
        """Exports the created Deck to .apkg"""
        os.makedirs(self.output_dir, exist_ok=True)
        filename = f'{self.deck_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.apkg'
        path = os.path.join(self.output_dir, filename)
        genanki.Package(self.deck).write_to_file(path)
        return path
