class Card:

    def __init__(self, word: str, front: str, back: str):
        self.word = word
        self.front = front
        self.back = back

    def __repr__(self) -> str:
        return f'Card(word: {self.word}), front: {self.front} back: {self.back}'

    def to_dict(self) -> dict:
        return {
            'word': self.word,
            'front': self.front,
            'back': self.back
        }
