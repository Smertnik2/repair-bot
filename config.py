import os

TG_BOT_TOKEN = '8671490880:AAG4szvpCbRve31dRzdTPXyfAxDzpWWdvUk'
FB_PAGE_TOKEN = 'EAAadLlLcCXMBRSrWyfnYo07AgireR25pGsbAfMKqIeZAsntZAd63jWqTyFgTwqGeXQrgcfDLrA0oZAPEWslYgvZCpMSg09va7ZC5UxAVAEzDSczBUutMgjZBwhJ8bG3qf6ZAPIwWaSginJuRmvdIyscpOThOjZBxG9PMjI4PqqxSb4lQYrvdJEcFGghZBkEIa0qwXdDROZB1BKqZBTVsP1ZAV76ZCHtbtZAAZDZD'
FB_VERIFY_TOKEN = 'repairfix123'

ADMIN_IDS = os.getenv('ADMIN_IDS', '5006092089').split(',')

PROXIES = {
    'http': 'http://proxy.server:3128',
    'https': 'http://proxy.server:3128'
}

DB_PATH = '/home/smertnik/bot/bot.db'
