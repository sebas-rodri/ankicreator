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
model_names = {"gpt-3.5-turbo":"gpt3.5 (max 4,097 tokens)","gpt-3.5-turbo-16k":"gpt3.5 (max 16,385 tokens)","gpt-4": "gpt-4 (max 8,192 tokens)","gpt-4-32k":"gpt-4 (max 32,768 tokens)"}
MODEL = ui.select(options=model_names,with_input=True,value="gpt-3.5-turbo")
#ui.label(MODEL)
MODEL_ID = random.randrange(1 << 30, 1 << 31)
DECK_ID = random.randrange(1 << 30, 1 << 31)
global anki_deck
global anki_model
anki_deck = functions.initialize_deck(DECK_ID,"test")
anki_model = functions.initialize_model_frontback(MODEL_ID)

user_textarea_input = ui.textarea(label="Text to process: ", placeholder="input here")

'''
front_back_prompt.append(functions.user_content(call_stack))

response = openai.ChatCompletion.create(
    model=MODEL,
    messages=front_back_prompt,
    temperature=0,
)

flashcard_list = eval(response["choices"][0]["message"]["content"])


functions.fill_deck(flashcard_list,anki_model,anki_deck)
genanki.Package(anki_deck).write_to_file('output.apkg')
'''
ui.run(favicon='🚀',title="Anki Flashcard Creator")