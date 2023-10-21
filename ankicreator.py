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
        self.not_finished = True
    
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
        print(self.user_input)
    
        

def create_flashcards_button(self: Prompt):
    if prompt.user_input == None or prompt.user_input.strip() == "":
        ui.notify("You need to input text or PDF")
        return
    self.make_full_prompt()
    print(self.full_prompt)
    create_flashcards(self)
    genanki.Package(settings.anki_deck).write_to_file('output.apkg')
    settings.not_finished = False
    ui.notify("Succes, Flashcards created")

def create_flashcards(self: Prompt):
    response = openai.ChatCompletion.create(
    model=settings.MODEL,
    messages=self.full_prompt,
    temperature=0,
    )
    flashcard_list = eval(response["choices"][0]["message"]["content"])
    functions.fill_deck(flashcard_list,settings.anki_model,settings.anki_deck)


def num_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(settings.MODEL)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def calculate_price():
    basic_prompt_tokenlen = num_tokens_from_string(str(prompt.basic_prompt))
    if prompt.user_input == None:
        if settings.MODEL == "gpt-3.5-turbo":
            return str(0.0015 * basic_prompt_tokenlen / 1000)
        elif settings.MODEL == "gpt-3.5-turbo-16k":
            return str(0.003 * basic_prompt_tokenlen /1000)
        elif settings == "gpt-4":
            return str(0.003 * basic_prompt_tokenlen / 1000)
        elif settings.MODEL == "gpt-4-32k":
            return str(0.006 * basic_prompt_tokenlen / 1000)
    elif prompt.user_input:
        user_input_tokenlen = num_tokens_from_string(str(prompt.user_input))
        if settings.MODEL == "gpt-3.5-turbo":
            return str(0.0015 * basic_prompt_tokenlen / 1000 + 0.002 * user_input_tokenlen)
        elif settings.MODEL == "gpt-3.5-turbo-16k":
            return str(0.003 * basic_prompt_tokenlen /1000 + 0.004 * user_input_tokenlen)
        elif settings == "gpt-4":
            return str(0.003 * basic_prompt_tokenlen / 1000 + 0.06 * user_input_tokenlen)
        elif settings.MODEL == "gpt-4-32k":
            return str(0.006 * basic_prompt_tokenlen / 1000 + 0.12 * user_input_tokenlen)
    return None

settings = Settings()
prompt = Prompt()

model_names = {"gpt-3.5-turbo":"gpt3.5 (max 4,097 tokens)","gpt-3.5-turbo-16k":"gpt3.5 (max 16,385 tokens)","gpt-4": "gpt-4 (max 8,192 tokens)","gpt-4-32k":"gpt-4 (max 32,768 tokens)"}
prompt_options = {"front_back_prompt": "Basic Front Back Flashcard"}



@ui.page('/',dark=True)
async def page_layout():
    
    with ui.row().classes('w-full justify-center'):
        ui.select(options=model_names,value="gpt-3.5-turbo",with_input=True,on_change=lambda e: settings.change_model(e.value)).classes('w-64 pt-6')
    with ui.row().classes('w-full justify-center'):
        ui.select(options=prompt_options,with_input=True,value="front_back_prompt",on_change=lambda e: prompt.set_basic_prompt(e.value)).classes('w-64')
    with ui.row().classes('w-full justify-center'):
        textarea = ui.textarea(label="Text to process: ", placeholder="input here",on_change=lambda e: prompt.set_user_input(e.value)).classes('w-96 h-96')
    with ui.row().classes('w-full justify-center'):
        flashcard_button = ui.button("Create Flashcards")
    print(calculate_price())
    while(settings.not_finished):
        await flashcard_button.clicked()
        create_flashcards_button(prompt)





ui.run(favicon='🚀',title="Anki Flashcard Creator",host="127.0.0.1",port=8081)