import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('GROQ_API_KEY')
openai.api_base = 'https://api.groq.com/openai/v1'

def generate_card_content(word: str, prompt: str, modifiers: list[str] = []) -> dict:
    full_prompt = f'{prompt.strip()}\nWord: {word.strip()}\n' + '\n'.join(modifiers)
    print(f'Aqui esta o prompt: {full_prompt}')
    try:
        response = openai.ChatCompletion.create(
            model='llama-3.3-70b-versatile',
            messages=[
                {'role': 'system', 'content': 'You are an assisstant that creates flashcards for language learning study.'},
                {'role': 'user', 'content': full_prompt}
            ],
            temperature=0.7,
        )

        answer = response.choices[0].message.content.strip()

        if 'Front:' in answer and 'Back:' in answer:
            parts = answer.split('Front:')[1].split('Back:')
            front = parts[0].strip()
            back = parts[1].strip()
        else:
            front = ''
            back = answer  

        print(answer)
        return {'words': word, 'front': front, 'back': back}
    
    except Exception as e:
        print(f'Failure generating the card for {word}: {e}')
        return {'words': word, 'front': '', 'back': '[Error generating content]'}
    
def generate_multiple_cards(words: list[str], prompt: str, modifiers: list[str] = []) -> list[dict]:
    return [generate_card_content(word, prompt, modifiers) for word in words]