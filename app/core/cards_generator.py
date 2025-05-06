import os

import openai
from dotenv import load_dotenv

from app.core.card import Card

load_dotenv()

openai.api_key = os.getenv('GROQ_API_KEY')
openai.api_base = 'https://api.groq.com/openai/v1'


class CardGenerator:
    def __init__(self, model: str = 'llama-3.3-70b-versatile'):
        # It is recommended to use the 'llama-3.3-70b-versatile' model.
        self.model = model

    def _get_prompt(self, word: str, prompt: str, modifiers: list[str]) -> str:
        return f'{prompt.strip()}\nWord: {word.strip()}\n' + '\n'.join(modifiers)

    def _call_api(self, full_prompt: str) -> str:
        response = openai.ChatCompletion.create(
            model='llama-3.3-70b-versatile',
            messages=[
                {
                    'role': 'system',
                    'content': (
                        'You are an assisstant that creates flashcards for language learning study.'
                    ),
                },
                {'role': 'user', 'content': full_prompt},
            ],
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()

    def _parse_answer(self, answer: str, word: str) -> Card:
        if 'Front:' in answer and 'Back:' in answer:
            parts = answer.split('Front:')[1].split('Back:')
            front = parts[0].strip()
            back = parts[1].strip()
        else:
            front = ''
            back = answer

        return Card(word=word, front=front, back=back)

    def generate_card(self, word: str, prompt: str, modifiers: list[str] = []) -> Card:
        full_prompt = self._get_prompt(word, prompt, modifiers)

        try:
            answer = self._call_api(full_prompt)
            return self._parse_answer(answer, word)
        except Exception as e:
            print(f'Error generating the card content for the word {word}: {e}')
            return Card(word, front='', back='Error generating the content')

    def generate_cards(
        self, words: list[str], prompt: str, modifiers: list[str] = []
    ) -> list[Card]:
        return [self.generate_card(word, prompt, modifiers) for word in words]
