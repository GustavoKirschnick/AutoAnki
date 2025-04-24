import random
from datetime import datetime

import genanki


def export_to_anki(cards: list[dict], deck: str = None, tag: str = None, output_dir: str = 'exports') -> str:
    model_id = random.randrange(1 << 30, 1 << 31)
    deck_id = random.randrange(1 << 30, 1 << 31)

    model = genanki.Model(
        model_id,
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

    anki_deck = genanki.Deck(deck_id, deck or 'Default_Deck')

    for card in cards:
        note = genanki.Note(
            model=model,
            fields=[card['front'], card['back']],
            tags=[tag] if tag else []
        )
        anki_deck.add_note(note)

    import os
    os.makedirs(output_dir, exist_ok=True)

    filename = f'{deck.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.apkg'
    path = os.path.join(output_dir, filename)

    genanki.Package(anki_deck).write_to_file(path)
    return path
