# Wanikani Radicals Parser

## About
It is a wanikani radicals parser. Pretty obvious, right?

I started learning kanji and discovered about a mnemonics method (it is a method, where you memorize things using stories).
WaniKani uses this method, but you need some money to use WaniKani app. So I decided to
parse all radicals, kanji, and vocabulary to make Anki deck.

## Parsing
### Radicals
All the radicals are taken from this [page](https://www.wanikani.com/radicals).
Every radical information taken from its page, [example](https://www.wanikani.com/radicals/barb).

The parser takes next fields about a radical:
```bash
     Column      |            Type             |                 
-----------------|-----------------------------|
 id              | integer                     |
 level           | integer                     | 
 symbol          | character varying           | 
 meaning         | character varying           | 
 mnemonic        | character varying           | 
 image_filename  | character varying           | 
 is_symbol_image | boolean                     | 
 url             | character varying           | 
 created_at      | timestamp without time zone | 
```

Some radicals are custom WaniKani radicals, so they do not have official UTF-8 symbol.
Instead, these radicals are stored as images. For example, [gun](https://www.wanikani.com/radicals/gun) radical.

The parser saves the parsed data into a ```output/wanikani_radicals.csv``` file.
The rows have the same order as in the list above. Images are saved into a ```output/images``` folder.

The meanings of the radicals are highlighted in WaniKani, and in the parsed data they are also highlighted with capital letters.  
### Kanji
All the kanji are taken from this [page](https://www.wanikani.com/kanji).
Every kanji information taken from its page, [example](https://www.wanikani.com/kanji/%E4%B8%8A).

Kanji data is splitted into four tables:
- `kanji` — general information about kanji
```bash
  Column    |            Type             |   
------------+-----------------------------|
 id         | integer                     |     
 level      | integer                     |    
 symbol     | character varying           |     
 url        | character varying           |     
 created_at | timestamp without time zone |       
```
- `kanji_meanings` — different meanings of kanji
```bash
    Column     |            Type             |                 
---------------|-----------------------------|
 id            | integer                     |
 kanji_id      | integer                     |
 meaning       | character varying           |
 is_primary    | boolean                     |
 mnemonic      | character varying           |
 mnemonic_hint | character varying           |
 created_at    | timestamp without time zone |
 ```
- `kanji_radicals` — radicals which used in kanji
``` bash
    Column     |            Type             |            
---------------|-----------------------------|
 id            | integer                     |
 kanji_id      | integer                     | 
 wk_radical_id | integer                     | 
 created_at    | timestamp without time zone |
 ```
- `kanji_readings` — different readings of kanji
```bash
    Column     |            Type             |            
---------------|-----------------------------|
 id            | integer                     |
 kanji_id      | integer                     | 
 reading       | character varying           | 
 type          | character varying           | 
 mnemonic      | character varying           | 
 mnemonic_hint | character varying           | 
 is_primary    | boolean                     | 
 created_at    | timestamp without time zone |
```

### Vocabulary
All vocabulary words are taken from this [page](https://www.wanikani.com/vocabulary).
Every kanji information taken from its page, [example](https://www.wanikani.com/vocabulary/%E4%B8%8A).

Vocabulary word data is splitted into four tables:
- `words` — general information about vocabulary word.
```bash
         Column         |            Type             |          
------------------------|-----------------------------|
 id                     | integer                     |
 level                  | integer                     | 
 url                    | character varying           | 
 symbols                | character varying           | 
 reading                | character varying           | 
 reading_explanation    | character varying           | 
 reading_audio_filename | character varying           | 
 types                  | character varying           | 
```
- `word_meanings` — different vocabulary word meanings.
```bash
   Column    |            Type             |                  
-------------|-----------------------------|
 id          | integer                     |
 word_id     | integer                     | 
 meaning     | character varying           | 
 is_primary  | boolean                     | 
 explanation | character varying           | 
 created_at  | timestamp without time zone |
```
- `word_use_patterns` — different use patterns of vocabulary word
```bash
   Column   |            Type             | 
------------|-----------------------------|
 id         | integer                     |
 word_id    | integer                     | 
 pattern    | character varying           | 
 japanese   | character varying           | 
 english    | character varying           | 
 created_at | timestamp without time zone |
```
- `word_context_sentences` — context sentences with vocabulary word 
```bash
   Column   |            Type             |              
------------|-----------------------------|
 id         | integer                     |
 word_id    | integer                     | 
 japanese   | character varying           | 
 english    | character varying           | 
 created_at | timestamp without time zone |
```
## Installation and usage
First, clone the repository to your machine where you want host the telegram bot and go to the project directory:
``` bash
git clone https://github.com/jakefish18/wanikani-parser
cd wanikani-parser
```

Second, it is not a required step, but I highly recommend to create `venv/` for the project
```bash
python3 -m venv venv/
source venv/bin/activate
```
In case you have fish shell:
```bash
python3 -m venv venv/
source venv/bin/activate.fish
```

Third, install the requirements
``` bash
pip3 install -r requirements.txt 
```

Fourth, create a `.env` file in `src` folder and fill it using `.env.example` as an example:
``` bash
# Database settings.
DATABASE_URL = "driver://user:pass@host:port/database_name"
```
As you can see, you need a postgresql database.

Fifth, change `is_download_image` and `is_download_audio` flags in `main.py` by your need.

Last, run the bot:
```bash
python3 main.py
```

You're ready! Keep the parser for some time because it rechecks for missed radicals, kanji, and vocabulary. You can see logs in `logs/` folder and output images and audio in `output/` folder.

## Anki Deck Creation
```anki_deck_creator.py``` does not work yet. Seems like the library for generating anki decks have some troubles. Nevertheless, you can make your anki deck by `export_to_csv.py` script. Customize it for your needs by chaning `before_level` and `deck_element` variables.

Example of possible anki cards:
![Front side](images/card_question.png)
![Back side](images/card_answer.png)

DM me in Telegram if you have some questions.