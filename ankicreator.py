import openai
import os
from nicegui import ui
import tiktoken
import genanki
import random
import functions 
from prompts import front_back_prompt
from test import call_stack, anki_test

os.chdir(os.path.dirname(os.path.abspath(__file__)))
#Settings
openai.api_key = os.getenv('OPEN_API_KEY')
MODEL = "gpt-3.5-turbo"
MODEL_ID = random.randrange(1 << 30, 1 << 31)
DECK_ID = random.randrange(1 << 30, 1 << 31)
global anki_deck
global anki_model
anki_deck = functions.initialize_deck(DECK_ID,"test")
anki_model = functions.initialize_model_frontback(MODEL_ID)

front_back_prompt.append(functions.user_content(call_stack))

print(front_back_prompt)


response = openai.ChatCompletion.create(
    model=MODEL,
    messages=front_back_prompt,
    temperature=0,
)

print(response["choices"][0]["message"]["content"])
flashcard_list = eval(response["choices"][0]["message"]["content"])


functions.fill_deck(flashcard_list,anki_model,anki_deck)
genanki.Package(anki_deck).write_to_file('output.apkg')