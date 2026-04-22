import requests
import json
from config import *

PROXIES = {
    'http': 'http://proxy.server:3128',
    'https': 'http://proxy.server:3128'
}

def tg_send(chat_id, text, reply_markup=None, parse_mode=None):
    url = f'https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage'
    data = {'chat_id': chat_id, 'text': text}
    if reply_markup:
        data['reply_markup'] = json.dumps(reply_markup)
    if parse_mode:
        data['parse_mode'] = parse_mode
    requests.post(url, data=data, proxies=PROXIES, timeout=10)

def tg_send_document(chat_id, file_content, filename, caption=None):
    url = f'https://api.telegram.org/bot{TG_BOT_TOKEN}/sendDocument'
    files = {'document': (filename, file_content)}
    data = {'chat_id': chat_id}
    if caption:
        data['caption'] = caption
    requests.post(url, data=data, files=files, proxies=PROXIES, timeout=10)

def send_msg(platform, user_id, text, quick_replies=None, **kwargs):
    if platform == 'tg':
        tg_send(user_id, text, **kwargs)
    elif platform == 'fb':
        if quick_replies:
            data = {
                'recipient': {'id': user_id},
                'message': {'text': text, 'quick_replies': quick_replies}
            }
        else:
            data = {
                'recipient': {'id': user_id},
                'message': {'text': text}
            }
        requests.post(
            'https://graph.facebook.com/v18.0/me/messages',
            params={'access_token': FB_PAGE_TOKEN},
            json=data,
            proxies=PROXIES,
            timeout=10
        )

def show_lang_select(platform, user_id):
    keyboard = {
        'keyboard': [['🇺🇦 Українська'], ['🇷🇺 Русский'], ['🇵🇱 Polski']],
        'resize_keyboard': True,
        'one_time_keyboard': True
    }
    tg_send(user_id, "Оберіть мову / Выберите язык / Wybierz język", reply_markup=keyboard)