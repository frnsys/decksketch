import json
import requests
from tqdm import tqdm
from datetime import datetime

CACHE_EXPIRE = 60*60*12
CACHE_FILE = '.cache.json'
try:
    with open(CACHE_FILE, 'r') as f:
        cache = json.load(f)
except FileNotFoundError:
    cache = {}

def get_card(name):
    now = datetime.now().timestamp()

    # Return cached if present and fresh
    if name in cache:
        data = cache[name]
        if now - data['retrieved'] < CACHE_EXPIRE:
            return data['card']

    resp = requests.get('https://api.scryfall.com/cards/named', params={'exact': name})
    if resp.status_code == 404:
        return None

    card = resp.json()
    cache[name] = {
        'retrieved': now,
        'card': card
    }
    return card


def render_card(card):
    return '''<li>
        <img src="{}"/>
        <div>{}</div>
    </li>'''.format(
        card['image_uris']['small'],
        card['prices']['usd'])

def render_spoiler(cards):
    prices = [c['prices']['usd'] for c in cards]
    total = sum(float(p) for p in prices if p)
    unknown = sum(1 for p in prices if not p)

    style = '''
        html {
            font-family: monospace;
        }
        ul, li {
            margin: 0;
            padding: 0;
        }
        ul {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
        }
        li {
            list-style-type: none;
            margin-bottom: 0.5em;
        }
        main {
            margin: 0 auto;
            max-width: 980px;
        }
    '''
    html = '''<html>
        <head>
            <title>deck</title>
            <style>{style}</style>
        </head>
        <body>
            <main>
                <ul>
                    {cards}
                </ul>
                <div>{total}</div>
            </main>
        </body>
    </html>'''.format(style=style,
                      cards='\n'.join(render_card(c) for c in cards),
                      total='{:.2f}, with {} unknown prices'.format(total, unknown))
    with open('deck.html', 'w') as f:
        f.write(html)


if __name__ == '__main__':
    import sys
    decklist = sys.argv[1]
    with open(decklist, 'r') as f:
        deck = [l for l in f.read().splitlines() if l and not l.startswith('#')]

    cards = []
    for name in tqdm(deck):
        card = get_card(name)
        if card is not None:
            cards.append(card)

    render_spoiler(cards)

    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f)