import openai
import os
from nicegui import ui
import tiktoken
import genanki
import random
import functions 
from prompts import prompts
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
    
    def change_model(self, value):
        self.MODEL = value
        print(self.MODEL)


class Prompt:
    def __init__(self):
        self.basic_prompt = prompts["front_back_prompt"]
        self.user_input = None
        self.full_prompt = None

    def make_full_prompt(self):
        self.full_prompt = self.basic_prompt
        self.full_prompt.append(functions.user_content(self.user_input))
    
    def set_basic_prompt(self, value: str):
        self.basic_prompt = prompts[value]
    
    def set_user_input(self, value: str):
        self.user_input = value

def create_flashcards_button(self: Prompt):
    self.make_full_prompt()
    print(self.full_prompt)
    create_flashcards(self)
    genanki.Package(settings.anki_deck).write_to_file('output.apkg')
    ui.notify("Succes, Flashcards created")

def create_flashcards(self: Prompt):
    response = openai.ChatCompletion.create(
    model=settings.MODEL,
    messages=self.full_prompt,
    temperature=0,
    )
    flashcard_list = eval(response["choices"][0]["message"]["content"])
    functions.fill_deck(flashcard_list,settings.anki_model,settings.anki_deck)

settings = Settings()
prompt = Prompt()

model_names = {"gpt-3.5-turbo":"gpt3.5 (max 4,097 tokens)","gpt-3.5-turbo-16k":"gpt3.5 (max 16,385 tokens)","gpt-4": "gpt-4 (max 8,192 tokens)","gpt-4-32k":"gpt-4 (max 32,768 tokens)"}
prompt_options = {"front_back_prompt": "Basic Front Back Flashcard"}



@ui.page('/',dark=True)
async def button():
    ui.select(options=model_names,value="gpt-3.5-turbo",with_input=True,on_change=lambda e: settings.change_model(e.value)).classes('w-40')
    ui.select(options=prompt_options,with_input=True,value="front_back_prompt",on_change=lambda e: prompt.set_basic_prompt(e.value))
    ui.textarea(label="Text to process: ", placeholder="input here",on_change=lambda e: prompt.set_user_input(e.value))
    flashcard_button = ui.button("Create Flashcards")
    await flashcard_button.clicked()
    create_flashcards_button(prompt)





ui.run(favicon='🚀',title="Anki Flashcard Creator",host="127.0.0.1",port=8081)