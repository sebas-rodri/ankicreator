import genanki
def user_content(text: str)->dict:
    return {"role":"user", "content": text}

def initialize_model_frontback(MODEL_ID: int):
    anki_model= genanki.Model(
    MODEL_ID,
    'Simple Model',
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
    ],
    templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Question}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
    },
  ])
    return anki_model

def initialize_deck(DECK_ID: int, name: str):
    anki_deck = genanki.Deck(
    DECK_ID,
    name)
    return anki_deck


def fill_deck(flashcard_list: list,anki_model,anki_deck)->None:
    for flashcard in flashcard_list:

        my_note = genanki.Note(
        model=anki_model,
        fields=flashcard)

        anki_deck.add_note(my_note)