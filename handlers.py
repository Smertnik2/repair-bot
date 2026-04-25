# handlers.py
import os, re, sys, traceback
from config import ADMIN_IDS
from texts import t, LANGS
from ui import send_text, send_lang_select, send_menu, send_device_select, send_request_preview, tg_answer_callback
from database import create_order, get_user_orders, is_loyal_client

processing_users = {}
user_state = {}
user_data = {}
user_lang = {}
stopped_users = set()
processed_callbacks = set()

DEVICE_MAP = {
    'DEVICE_phone': 'btn_phone',
    'DEVICE_tablet': 'btn_tablet',
    'DEVICE_laptop': 'btn_laptop',
    'DEVICE_pc': 'btn_pc',
    'DEVICE_console': 'btn_console',
    'DEVICE_other': 'btn_other'
}

def log_error(e):
    print(f"ERROR: {str(e)}", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)

def cache_get(cache, key, default=None):
    return cache.get(key, default)

def cache_set(cache, key, value):
    cache[key] = value

def clear_user_data(user_key):
    user_state.pop(user_key, None)
    user_data.pop(user_key, None)

def validate_phone(text):
    digits = re.sub(r'\D', '', text)
    if len(digits) >= 9 and len(digits) <= 15:
        return True, '+' + digits if not text.startswith('+') else text
    return False, text

def handle_start(platform, user_id):
    user_key = f"{platform}_{user_id}"
    cache_set(user_state, user_key, 'lang_select')
    send_lang_select(platform, user_id)

def handle_lang_select(platform, user_id, text):
    user_key = f"{platform}_{user_id}"
    lang = None
    if text in ['LANG_ua', '🇺🇦 Українська', '🇺🇦 Украинский', '🇺🇦 Ukraiński']:
        lang = 'ua'
    elif text in ['LANG_ru', '🇷🇺 Російська', '🇷🇺 Русский', '🇷🇺 Rosyjski']:
        lang = 'ru'
    elif text in ['LANG_pl', '🇵🇱 Польська', '🇵🇱 Польский', '🇵🇱 Polski']:
        lang = 'pl'
    
    if lang:
        cache_set(user_lang, user_key, lang)
        cache_set(user_state, user_key, 'menu')
        send_text(platform, user_id, t(lang, 'lang_set'))
        send_text(platform, user_id, t(lang, 'start_msg'))
        send_menu(platform, user_id, lang)
        return True
    return False

def handle_message(platform, user_id, text, message_id=None, photo=None, callback_data=None):
    try:
        user_key = f"{platform}_{user_id}"
        lang = cache_get(user_lang, user_key, 'ru')
        
        if user_key in stopped_users and text not in ['/start', '/restart']:
            return
        
        # Обработка callback от inline кнопок TG
        if callback_data:
            if callback_data == 'CONFIRM_ORDER':
                data = cache_get(user_data, user_key, {})
                order_id = create_order(
                    platform=platform,
                    user_id=user_id,
                    device=t(lang, data.get('device_key', 'btn_other')),
                    brand=data.get('brand', ''),
                    problem=data.get('problem', ''),
                    phone=data.get('phone', ''),
                    name=data.get('name', '')
                )
                send_text(platform, user_id, t(lang, 'order_sent', id=order_id))
                clear_user_data(user_key)
                cache_set(user_state, user_key, 'menu')
                send_menu(platform, user_id, lang)
                return
            elif callback_data == 'CANCEL_ORDER':
                clear_user_data(user_key)
                cache_set(user_state, user_key, 'menu')
                send_text(platform, user_id, t(lang, 'order_cancelled'))
                send_menu(platform, user_id, lang)
                return
            elif callback_data == 'EDIT_ORDER':
                cache_set(user_state, user_key, 'device')
                send_device_select(platform, user_id, lang)
                return
        
        state = cache_get(user_state, user_key, 'start')
        text_clean = text.strip()
        
        # Команды
        if text_clean.lower() in ['/start', 'start', 'старт']:
            handle_start(platform, user_id)
            return
        
        # Выбор языка
        if state == 'lang_select' or text_clean in ['/lang', 'мова', 'язык', 'język', 'CHANGE_LANG']:
            if handle_lang_select(platform, user_id, text_clean):
                return
            handle_start(platform, user_id)
            return
        
        # Главное меню
        if text_clean in [t(lang, 'btn_new_order'), 'NEW_ORDER']:
            cache_set(user_state, user_key, 'device')
            cache_set(user_data, user_key, {})
            send_device_select(platform, user_id, lang)
            return
        
        if text_clean in [t(lang, 'btn_my_orders'), 'MY_ORDERS']:
            orders = get_user_orders(platform, user_id)
            if not orders:
                send_text(platform, user_id, t(lang, 'no_orders'))
            else:
                msg = t(lang, 'your_orders') + '\n\n'
                for o in orders[:10]:
                    msg += f"#{o['id']} - {o['device']} - {o['status']}\n"
                send_text(platform, user_id, msg)
            send_menu(platform, user_id, lang)
            return
        
        if text_clean in [t(lang, 'btn_change_lang'), 'CHANGE_LANG']:
            cache_set(user_state, user_key, 'lang_select')
            send_lang_select(platform, user_id)
            return
        
        if text_clean in [t(lang, 'btn_back'), 'BACK_MENU']:
            cache_set(user_state, user_key, 'menu')
            send_menu(platform, user_id, lang)
            return
        
        # Стейты создания заявки
        if state == 'device':
            device_key = DEVICE_MAP.get(text_clean)
            if not device_key:
                for k, v in DEVICE_MAP.items():
                    if t(lang, v) == text_clean:
                        device_key = v
                        break
            if device_key:
                data = cache_get(user_data, user_key, {})
                data['device_key'] = device_key
                cache_set(user_data, user_key, data)
                cache_set(user_state, user_key, 'brand')
                send_text(platform, user_id, t(lang, 'ask_brand_model'))
            else:
                send_device_select(platform, user_id, lang)
            return
        
        if state == 'brand':
            data = cache_get(user_data, user_key, {})
            data['brand'] = text_clean
            cache_set(user_data, user_key, data)
            cache_set(user_state, user_key, 'problem')
            send_text(platform, user_id, t(lang, 'ask_problem'))
            return
        
        if state == 'problem':
            data = cache_get(user_data, user_key, {})
            data['problem'] = text_clean
            cache_set(user_data, user_key, data)
            cache_set(user_state, user_key, 'phone')
            send_text(platform, user_id, t(lang, 'ask_phone'))
            return
        
        if state == 'phone':
            valid, phone = validate_phone(text_clean)
            if not valid:
                send_text(platform, user_id, t(lang, 'error_phone'))
                return
            data = cache_get(user_data, user_key, {})
            data['phone'] = phone
            cache_set(user_data, user_key, data)
            cache_set(user_state, user_key, 'name')
            send_text(platform, user_id, t(lang, 'ask_name'))
            return
        
        if state == 'name':
            data = cache_get(user_data, user_key, {})
            data['name'] = text_clean
            cache_set(user_data, user_key, data)
            cache_set(user_state, user_key, 'preview')
            send_request_preview(platform, user_id, lang, data)
            return
        
        # По умолчанию - меню
        cache_set(user_state, user_key, 'menu')
        send_menu(platform, user_id, lang)
        
    except Exception as e:
        log_error(e)
