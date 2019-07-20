# decksketch

Script for viewing and pricing MTG decks

## Usage

    python main.py path/to/decklist.txt

- Each line should contain one card name (right now this assumes singleton format, so no card quantities are supported).
- Lines starting with `#` are considered comments and are ignored.
- The script outputs a file, `deck.html`, that you can view in a browser.
- The script caches card data for 12 hours.