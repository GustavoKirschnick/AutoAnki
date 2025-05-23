# AutoAnki

AutoAnki is a tool for automatic generation of Anki flashcards using Groq’s API, based on user-defined word input and customizable prompts, designed to assist language learning.

## Features
- Generate Anki flashcards using Groq’s API
- Customize prompts and its modifiers
- User interface with Streamlit
- Export cards in .apkg format compatible with Anki
- SQLite database for prompt and prompt modifiers persistence
- Automated testing with Pytest

## Preview
### Generating the cards
![Preview](assets/cards_generation_showcase.gif)
*Enter the words, select a prompt and its modifiers to generate the cards*
### Creating a prompt
![Preview](assets/prompt_creating_showcase.gif)
*Create the prompts and prompt modifiers. They can also be listed, edited and deleted*
## Getting started

### 1. Clone the repo
```
git clone https://github.com/GustavoKirschnick/AutoAnki.git
cd AutoAnki
```

### 2. Install the dependencies
Make sure that you have [Poetry](https://python-poetry.org/docs/#installing-with-pipx) dependency manager installed.
```
poetry install
```
### 3. Create a .env file
Create a file called `.env` in the root of the repository, with:
```
DATABASE_URL='sqlite:///./database.db'
GROQ_API_KEY = your_key_value
```
#### 3.1 Generate a Groq API key
For the application to run, it is necessary to generate a Groq API key, in the following website:
https://console.groq.com/keys

Save it on the `.env`file.

### 4. Initialize the database (run this step only once to initialize the database)
```
poetry shell
task init_db
```
> **Note**: to use any `task` command, the poetry environment must be activated prior to it (`poetry shell`).
### 5. Run the application
```
task run_app
```
> **Note**: alternatively, it is possible to run the application with the two sequential commands `task run`(to run the FastAPI server) and `task run_ui` (to run the user interface).
## Components
### Prompts: 
Customizable template that is sent to the API to generate the cards. An example prompt can be seen below: 
```text
Generate flashcards for the words below.
- Use the word in a sentence 
- Send the answer with the following format: 'front' and 'back'
- Front: only the example sentence with the word in German. Limit the example sentence for a maximal of 50 words
- Back: only the English translation.
```
**Note 1**: It is important to highlight that the prompt should contain the field `'Front'` and `'Back'`, so the code can parse the answer returned.  
**Note 2**: Only one prompt can be used.

### Prompt Modifiers: 
Similar to the prompts, defines an optional parameter that is combined with the Prompt (e.g tense, style or difficulty). Multiple prompt modifiers can be used at the same time. An example can be seen below:
```
Using the Konjuntiv 2 form
```
**Note**: Different from the `Prompts`, there is no need to include the fields `'Front'` or `'Back'`.

### Cards: 
The final result outputed by the code, which will be exported to Anki. It has a `'Front'` and `'Back'` field, with their respective content.


## Tech Stack

- **Python 3.12**, or superior version
- [FastAPI](https://fastapi.tiangolo.com) - API back-end
- [Streamlit](https://streamlit.io/) - Front-end interface
- [SQLite](https://www.sqlite.org) - Relational database
- [Pydantic](https://docs.pydantic.dev/) - Schema validation
- [Pytest](https://docs.pytest.org/) - Automatic testing
- [genanki](https://github.com/kerrickstaley/genanki) - generate Anki files
- [Poetry](https://python-poetry.org/) - Dependency manager
- [Pytask](https://pytask-dev.readthedocs.io/en/stable/#) - Task automation

### Running tests
---
Automated tests were implemented with `pydantic` for all endpoints.

To run all the tests:
```
task test
```
It is possible to run tests files separatelly:
```
pytest tests/test_routes_prompt_modifiers.py 
```
Or to run a specific test by name:
```
pytest -k test_create_prompt_modifier_valid
```
> This command runs only the `test_create_prompt_modifier_valid` function.

### Tasks
---
Refer to the `pyproject.toml` file for more details
### API Docs
---
Once the FastAPI server is running, the API documentation can be accessed at:  
**Swagger UI**: http://localhost:8000/docs


### To-do
---
- Integration with AnkiConnect to directly send the cards to the Anki app
- Enable the user to edit the generated cards before exporting them
- Enable the user to attribute different tags for different cards in the same deck
- Implement a fixture for the card router, to improve scalability of tests
---




