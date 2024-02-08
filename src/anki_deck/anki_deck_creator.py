import genanki

from src.models.wk_radical import WaniKaniRadical
from src.parsers.wk_radical_parser import wanikani_radicals_parser, import_from_csv
from random import randint


# Flag for reading all radical data from csv file.
READ_FROM_CSV_FILE = True


model_id = randint(1, 2 ** 32 - 1)
deck_id = randint(1, 2 ** 32 - 1)

wanikani_radicals_anki_model = genanki.Model(
    model_id=model_id,
    fields=[
        {"name": "Radical"},
        {"name": "Meaning"},
        {"name": "Mnemonic"}
    ],
    templates=[{
        "qfmt": "<h1>{{Radical}}</h1>",
        "afmt": "Meaning: <strong>{{Meaning}}</strong><br>Story: {{Mnemonic}}"
    }]
)
wanikani_radicals_anki_deck = genanki.Deck(
    deck_id=deck_id,
    name="WaniKani Radicals"
)

wanikani_radicals = []

if READ_FROM_CSV_FILE:
    wanikani_radicals: list[WaniKaniRadical] = import_from_csv()

else:
    wanikani_radicals: list[WaniKaniRadical] = wanikani_radicals_parser()

for wanikani_radical in wanikani_radicals:
    wanikani_radical_note = genanki.Note(
        model=wanikani_radicals_anki_model,
        fields=[wanikani_radical.symbol, wanikani_radical.meaning, wanikani_radical.mnemonic]
    )
    wanikani_radicals_anki_deck.add_note(wanikani_radical_note)

genanki.Package(wanikani_radicals_anki_deck).write_to_file("output/wanikani_radicals.apkg")