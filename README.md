# Wanikani Radicals Parser

## About
It is a wanikani radicals parser. Pretty obvious, right?

I started learning kanji and discovered about a mnemonics method (it is a method, where you memorize things using stories).
WaniKani uses this method, but you need some money to use WaniKani app. So I decided to
parse all radicals and kanji (in the future) to make Anki deck.

## Parsing
All the radicals are taken from this [page](https://www.wanikani.com/radicals).
Every radical information taken from its page, [example](https://www.wanikani.com/radicals/barb).

The parser takes next fields about a radical:
1. WaniKani level
2. Symbol (sometimes image of the symbol) 
3. Meaning
4. Story

Some radicals are custom WaniKani radicals, so they do not have official UTF-8 symbol.
Instead, these radicals are stored as images. For example, [gun](https://www.wanikani.com/radicals/gun) radical.

The parser saves the parsed data into a ```output/wanikani_radicals.csv``` file.
The rows have the same order as in the list above. Images are saved into a ```output/images``` folder.

The meanings of the radicals are highlighted in WaniKani, and in the parsed data they are also highlighted with capital letters.  

## Anki Deck Creation
```anki_deck_creator.py``` does not work yet. Seems like library for generating anki decks have some troubles. Nevertheless,
I have made Anki deck manually. You can access it by the [link](https://ankiweb.net/shared/info/219087015?cb=1707314019409). Since the missed radicals are added using the svg format, I needed
to do some magic with CSS to display it correctly.

After all actions, Anki card looks like this:<br>
<img alt="img.png" src="https://github.com/jakefish18/wanikani-radicals-parser/blob/main/card_appearnce_in_anki.png" width="400"/>

## Conclusion
Of course, these cards does not look very attractive, but you can freely use this parser to make your own Anki deck with your
own nice CSS styles.
 
