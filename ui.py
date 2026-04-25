# ui.py
import requests, json
from config import TG_BOT_TOKEN, FB_PAGE_TOKEN, PROXIES
from texts import t

def tg_send(chat_id, text, reply_markup=None, parse_mode=None):
    url = f'https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage'
    data = {'chat_id': chat_id, 'text': text}
    if reply_markup:
        data['reply_markup'] = json.dumps(reply_markup)
    if parse_mode:
        data['parse_mode'] = parse_mode
    try:
        requests.post(url, data=data, proxies=PROXIES, timeout=10)
    except Exception as e:
        print(f"TG send error: {e}")

def tg_answer_callback(callback_query_id):
    url = f'https://api.telegram.org/bot{TG_BOT_TOKEN}/answerCallbackQuery'
    requests.post(url, json={'callback_query_id': callback_query_id}, proxies=PROXIES, timeout=10)

def fb_send(user_id, data):
    try:
        requests.post(
            'https://graph.facebook.com/v18.0/me/messages',
            params={'access_token': FB_PAGE_TOKEN},
            json=data,
            proxies=PROXIES,
            timeout=10
        )
    except Exception as e:
        print(f"FB send error: {e}")

def send_text(platform, user_id, text, parse_mode=None):
    if platform == 'tg':
        tg_send(user_id, text, parse_mode=parse_mode)
    else:
        fb_send(user_id, {'recipient': {'id': user_id}, 'message': {'text': text}})

def send_lang_select(platform, user_id):
    langs = [
        {'key': 'ua', 'payload': 'LANG_ua', 'text_key': 'lang_ua'},
        {'key': 'ru', 'payload': 'LANG_ru', 'text_key': 'lang_ru'},
        {'key': 'pl', 'payload': 'LANG_pl', 'text_key': 'lang_pl'}
    ]
    if platform == 'tg':
        buttons = [[t('ua', l['text_key'])] for l in langs]
        keyboard = {'keyboard': buttons, 'resize_keyboard': True, 'one_time_keyboard': True}
        tg_send(user_id, t('ua', 'lang_select'), reply_markup=keyboard)
    else:
        replies = [{'content_type': 'text', 'title': t(l['key'], l['text_key'])[:20], 'payload': l['payload']} for l in langs]
        fb_send(user_id, {
            'recipient': {'id': user_id},
            'message': {'text': t('ua', 'lang_select'), 'quick_replies': replies[:11]}
        })

def send_menu(platform, user_id, lang):
    if platform == 'tg':
        buttons = [
            [t(lang, 'btn_new_order')],
            [t(lang, 'btn_my_orders')],
            [t(lang, 'btn_change_lang')]
        ]
        keyboard = {'keyboard': buttons, 'resize_keyboard': True}
        tg_send(user_id, t(lang, 'menu_text'), reply_markup=keyboard)
    else:
        replies = [
            {'content_type': 'text', 'title': t(lang, 'btn_new_order')[:20], 'payload': 'NEW_ORDER'},
            {'content_type': 'text', 'title': t(lang, 'btn_my_orders')[:20], 'payload': 'MY_ORDERS'},
            {'content_type': 'text', 'title': t(lang, 'btn_change_lang')[:20], 'payload': 'CHANGE_LANG'}
        ]
        fb_send(user_id, {
            'recipient': {'id': user_id},
            'message': {'text': t(lang, 'menu_text'), 'quick_replies': replies[:11]}
        })

def send_device_select(platform, user_id, lang):
    devices = [
        ('btn_phone', 'DEVICE_phone'),
        ('btn_tablet', 'DEVICE_tablet'),
        ('btn_laptop', 'DEVICE_laptop'),
        ('btn_pc', 'DEVICE_pc'),
        ('btn_console', 'DEVICE_console'),
        ('btn_other', 'DEVICE_other')
    ]
    if platform == 'tg':
        buttons = [[t(lang, d[0])] for d in devices]
        buttons.append([t(lang, 'btn_back')])
        keyboard = {'keyboard': buttons, 'resize_keyboard': True, 'one_time_keyboard': True}
        tg_send(user_id, t(lang, 'choose_device'), reply_markup=keyboard)
    else:
        replies = [{'content_type': 'text', 'title': t(lang, d[0])[:20], 'payload': d[1]} for d in devices]
        replies.append({'content_type': 'text', 'title': t(lang, 'btn_back')[:20], 'payload': 'BACK_MENU'})
        fb_send(user_id, {
            'recipient': {'id': user_id},
            'message': {'text': t(lang, 'choose_device'), 'quick_replies': replies[:11]}
        })

def send_request_preview(platform, user_id, lang, data):
    device_name = t(lang, data.get('device_key', 'btn_other'))
    text = f"{t(lang, 'preview_title')}\n\n"
    text += f"{t(lang, 'preview_device')}: {device_name}\n"
    text += f"{t(lang, 'preview_brand')}: {data.get('brand', '-')}\n"
    text += f"{t(lang, 'preview_problem')}: {data.get('problem', '-')}\n"
    text += f"{t(lang, 'preview_phone')}: {data.get('phone', '-')}\n"
    text += f"{t(lang, 'preview_name')}: {data.get('name', '-')}"
    
    if platform == 'tg':
        buttons = [
            [{'text': t(lang, 'btn_confirm'), 'callback_data': 'CONFIRM_ORDER'}],
            [{'text': t(lang, 'btn_edit'), 'callback_data': 'EDIT_ORDER'}],
            [{'text': t(lang, 'btn_cancel'), 'callback_data': 'CANCEL_ORDER'}]
        ]
        keyboard = {'inline_keyboard': buttons}
        tg_send(user_id, text, reply_markup=keyboard)
    else:
        buttons = [
            {'type': 'postback', 'title': t(lang, 'btn_confirm')[:20], 'payload': 'CONFIRM_ORDER'},
            {'type': 'postback', 'title': t(lang, 'btn_edit')[:20], 'payload': 'EDIT_ORDER'},
            {'type': 'postback', 'title': t(lang, 'btn_cancel')[:20], 'payload': 'CANCEL_ORDER'}
        ]
        payload = {
            'recipient': {'id': user_id},
            'message': {
                'attachment': {
                    'type': 'template',
                    'payload': {
                        'template_type': 'generic',
                        'elements': [{
                            'title': t(lang, 'preview_title'),
                            'subtitle': f"{device_name} | {data.get('brand', '-')}"[:80],
                            'buttons': buttons[:3]
                        }]
                    }
                }
            }
        }
        fb_send(user_id, payload)
