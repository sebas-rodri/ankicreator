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

class Settings:
    def __init__(self):
        self.MODEL = "gpt-3.5-turbo"
        self.MODEL_ID = random.randrange(1 << 30, 1 << 31)
        self.DECK_ID = random.randrange(1 << 30, 1 << 31)
        self.anki_deck = functions.initialize_deck(self.DECK_ID,"Ankicreator")
        self.anki_model = functions.initialize_model_frontback(self.MODEL_ID)
        openai.api_key = os.getenv('OPEN_API_KEY')

settings = Settings()

model_names = {"gpt-3.5-turbo":"gpt3.5 (max 4,097 tokens)","gpt-3.5-turbo-16k":"gpt3.5 (max 16,385 tokens)","gpt-4": "gpt-4 (max 8,192 tokens)","gpt-4-32k":"gpt-4 (max 32,768 tokens)"}
ui.select(options=model_names,with_input=True,value="gpt-3.5-turbo").bind_value(settings,'MODEL')

user_textarea_input = ui.textarea(label="Text to process: ", placeholder="input here")



front_back_prompt.append(functions.user_content(call_stack))

response = openai.ChatCompletion.create(
    model=settings.MODEL,
    messages=front_back_prompt,
    temperature=0,
)

flashcard_list = eval(response["choices"][0]["message"]["content"])


functions.fill_deck(flashcard_list,settings.anki_model,settings.anki_deck)
genanki.Package(settings.anki_deck).write_to_file('output.apkg')

ui.run(favicon='🚀',title="Anki Flashcard Creator")