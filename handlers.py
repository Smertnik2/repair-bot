import os
import sys
import traceback
from config import *
from texts import t, MENU_ITEMS, LANG_COMMANDS, STATUS_TRANS
from keyboards import send_msg, show_lang_select, tg_send
from database import create_order, get_user_orders, is_loyal_client

processing_users = {}
user_state = {}
user_data = {}
user_lang = {}
stopped_users = set()
processed_callbacks = set()

ADMIN_IDS = os.getenv('ADMIN_IDS', '5006092089').split(',')

def log_error(e):
    print(f"ERROR: {str(e)}", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)

def cache_get(cache, key, default=None):
    return cache.get(key, default)

def cache_set(cache, key, value):
    cache[key] = value

def clear_user_history(user_key):
    user_state.pop(user_key, None)
    user_data.pop(user_key, None)

def validate_phone(text, lang):
    import re
    digits = re.sub(r'\D', '', text)
    if len(digits) >= 12 or (len(digits) == 10 and not text.startswith('+')):
        return True, digits
    return False, text

def show_menu(platform, user_id, user_key):
    lang = cache_get(user_lang, user_key, 'ua')
    
    if platform == 'tg':
        buttons = [[item[lang]] for item in MENU_ITEMS.values()]
        buttons.append([t(lang, 'my_orders')])
        keyboard = {
            'keyboard': buttons,
            'resize_keyboard': True
        }
        tg_send(user_id, t(lang, 'choose_again'), reply_markup=keyboard)
    else:
        quick_replies = [{'content_type': 'text', 'title': item[lang], 'payload': f'DEVICE_{key}'} 
                        for key, item in MENU_ITEMS.items()]
        quick_replies.append({'content_type': 'text', 'title': t(lang, 'my_orders'), 'payload': 'MY_ORDERS'})
        send_msg(platform, user_id, t(lang, 'choose_again'), quick_replies=quick_replies)

def handle_message(platform, user_id, text, message_id=None, photo=None):
    try:
        user_key = f"{platform}_{user_id}"

        if user_key in stopped_users and text.lower() not in ['/restart', '/start', 'рестарт', 'restart']:
            return

        if message_id and platform == 'tg':
            import sqlite3
            conn = sqlite3.connect('/home/smertnik/bot/bot.db')
            c = conn.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS processed_msgs (msg_id INTEGER PRIMARY KEY)')
            try:
                c.execute('INSERT INTO processed_msgs VALUES (?)', (message_id,))
                conn.commit()
            except sqlite3.IntegrityError:
                conn.close()
                return
            conn.close()

        state = cache_get(user_state, user_key, 'start')
        text_lower = text.lower().strip()
        text_clean = text.strip()
        is_admin = str(user_id) in ADMIN_IDS

        # АДМІН КОМАНДИ
        if text_lower == '/admin' and is_admin:
            keyboard = {
                'inline_keyboard': [
                    [{'text': '📋 Останні 10 замовлень', 'callback_data': 'admin_orders'}],
                    [{'text': '📊 Статистика', 'callback_data': 'admin_stats'}],
                    [{'text': '📥 Експорт CSV', 'callback_data': 'admin_export'}]
                ]
            }
            tg_send(user_id, '🔧 <b>Адмін-панель</b>', reply_markup=keyboard, parse_mode='HTML')
            return

        if text_lower in ['/start', 'старт', 'start']:
            stopped_users.discard(user_key)
            if user_key in user_lang:
                show_menu(platform, user_id, user_key)
                cache_set(user_state, user_key, 'waiting_choice')
                cache_set(user_data, user_key, {'photos': [], 'description': '', 'phone': '', 'address': '', 'service_type': '', 'device': '', 'used_referral': None})
            else:
                show_lang_select(platform, user_id)
                cache_set(user_state, user_key, 'waiting_lang')
            return

        if text_lower == '/stop':
            stopped_users.add(user_key)
            lang = cache_get(user_lang, user_key, 'ua')
            send_msg(platform, user_id, t(lang, 'bot_stopped'))
            return

        if text_lower in ['/restart', 'рестарт', 'restart']:
            stopped_users.discard(user_key)
            clear_user_history(user_key)
            show_lang_select(platform, user_id)
            cache_set(user_state, user_key, 'waiting_lang')
            return

        if text_lower == '/clear':
            lang = cache_get(user_lang, user_key, 'ua')
            clear_user_history(user_key)
            send_msg(platform, user_id, t(lang, 'history_cleared'))
            return

        if text_lower in LANG_COMMANDS:
            show_lang_select(platform, user_id)
            cache_set(user_state, user_key, 'waiting_lang')
            return

        if text_clean in ['🇺🇦 Українська', 'Українська', 'UA']:
            old_lang = cache_get(user_lang, user_key)
            cache_set(user_lang, user_key, 'ua')
            if old_lang:
                send_msg(platform, user_id, t('ua', 'lang_changed'))
            show_menu(platform, user_id, user_key)
            cache_set(user_state, user_key, 'waiting_choice')
            cache_set(user_data, user_key, {'photos': [], 'description': '', 'phone': '', 'address': '', 'service_type': '', 'device': '', 'used_referral': None})
            return
        if text_clean in ['🇷🇺 Русский', 'Русский', 'RU']:
            old_lang = cache_get(user_lang, user_key)
            cache_set(user_lang, user_key, 'ru')
            if old_lang:
                send_msg(platform, user_id, t('ru', 'lang_changed'))
            show_menu(platform, user_id, user_key)
            cache_set(user_state, user_key, 'waiting_choice')
            cache_set(user_data, user_key, {'photos': [], 'description': '', 'phone': '', 'address': '', 'service_type': '', 'device': '', 'used_referral': None})
            return
        if text_clean in ['🇵🇱 Polski', 'Polski', 'PL']:
            old_lang = cache_get(user_lang, user_key)
            cache_set(user_lang, user_key, 'pl')
            if old_lang:
                send_msg(platform, user_id, t('pl', 'lang_changed'))
            show_menu(platform, user_id, user_key)
            cache_set(user_state, user_key, 'waiting_choice')
            cache_set(user_data, user_key, {'photos': [], 'description': '', 'phone': '', 'address': '', 'service_type': '', 'device': '', 'used_referral': None})
            return

        lang = cache_get(user_lang, user_key, 'ua')

        if state == 'waiting_choice':
            if text_lower == t(lang, 'my_orders').lower() or text_clean == 'MY_ORDERS':
                orders = get_user_orders(user_key)
                if not orders:
                    send_msg(platform, user_id, t(lang, 'no_orders'))
                else:
                    msg = t(lang, 'your_orders', count=len(orders))
                    for oid, device, status, discount, created in orders[:5]:
                        status_t = STATUS_TRANS.get(status, {}).get(lang, status)
                        msg += f"#{oid} {device}\n"
                        msg += t(lang, 'order_status', status=status_t)
                        if discount:
                            msg += t(lang, 'order_discount', discount=discount)
                        msg += t(lang, 'order_date', created=created[:10]) + '\n'
                    send_msg(platform, user_id, msg)
                return

            if text_clean.startswith('DEVICE_'):
                device_key = text_clean.split('_')[1]
                val = MENU_ITEMS.get(device_key)
            else:
                val = None
                for key, item in MENU_ITEMS.items():
                    if text_clean == item[lang]:
                        val = item
                        break

            if val:
                data = cache_get(user_data, user_key, {})
                data['device'] = val[lang]
                cache_set(user_data, user_key, data)
                cache_set(user_state, user_key, 'waiting_service_type')
                if platform == 'tg':
                    keyboard = {
                        'keyboard': [[t(lang, 'service_center')], [t(lang, 'service_home')]],
                        'resize_keyboard': True,
                        'one_time_keyboard': True
                    }
                    tg_send(user_id, t(lang, 'service_type'), reply_markup=keyboard)
                else:
                    send_msg(platform, user_id, t(lang, 'service_type'), quick_replies=[
                        {'content_type': 'text', 'title': t(lang, 'service_center'), 'payload': 'SERVICE_CENTER'},
                        {'content_type': 'text', 'title': t(lang, 'service_home'), 'payload': 'SERVICE_HOME'}
                    ])
                return
            send_msg(platform, user_id, t(lang, 'choose_again'))
            return

        if state == 'waiting_service_type':
            data = cache_get(user_data, user_key, {})
            if text_lower in [t(lang, 'service_center').lower(), 'service_center']:
                data['service_type'] = 'center'
                cache_set(user_data, user_key, data)
                cache_set(user_state, user_key, 'waiting_details')
                if platform == 'tg':
                    tg_send(user_id, t(lang, 'selected_device', device=data['device']), reply_markup={'remove_keyboard': True})
                else:
                    send_msg(platform, user_id, t(lang, 'selected_device', device=data['device']))
            elif text_lower in [t(lang, 'service_home').lower(), 'service_home']:
                data['service_type'] = 'home'
                cache_set(user_data, user_key, data)
                cache_set(user_state, user_key, 'waiting_details')
                if platform == 'tg':
                    tg_send(user_id, t(lang, 'selected_device', device=data['device']), reply_markup={'remove_keyboard': True})
                else:
                    send_msg(platform, user_id, t(lang, 'selected_device', device=data['device']))
            else:
                send_msg(platform, user_id, t(lang, 'service_type'))
            return

        if state == 'waiting_details':
            if text_lower in ['готово', 'готов', 'gotowe', 'done']:
                data = cache_get(user_data, user_key, {})
                desc = data.get('description', '').strip()
                photos = data.get('photos', [])
                
                if not desc and not photos:
                    send_msg(platform, user_id, t(lang, 'add_details'))
                    return
                    
                cache_set(user_state, user_key, 'waiting_phone')
                send_msg(platform, user_id, t(lang, 'almost_done'))
            else:
                data = cache_get(user_data, user_key, {})
                if 'description' not in data:
                    data['description'] = ''
                if 'photos' not in data:
                    data['photos'] = []
                    
                data['description'] += text + '\n'
                if photo:
                    data['photos'].append(photo)
                cache_set(user_data, user_key, data)
                send_msg(platform, user_id, t(lang, 'saved'))
            return

        if state == 'waiting_phone':
            data = cache_get(user_data, user_key)
            if not data:
                show_menu(platform, user_id, user_key)
                cache_set(user_state, user_key, 'waiting_choice')
                return

            is_valid, normalized_phone = validate_phone(text, lang)
            if not is_valid:
                send_msg(platform, user_id, t(lang, 'phone_invalid'))
                return

            data['phone'] = normalized_phone
            cache_set(user_data, user_key, data)

            if data.get('service_type') == 'home':
                cache_set(user_state, user_key, 'waiting_address')
                send_msg(platform, user_id, t(lang, 'ask_address'))
                return
            else:
                address = 'Сервісний центр'
                try:
                    order_id, discount, ref_code = create_order(
                        user_key, platform, data['device'], data['description'],
                        data['phone'], address, data['service_type'], data.get('used_referral')
                    )
                    msg = t(lang, 'order_accepted', order_id=order_id)
                    if discount:
                        msg += t(lang, 'your_discount', discount=discount)
                    msg += t(lang, 'your_ref', ref_code=ref_code)
                    msg += t(lang, 'master_contact')
                    send_msg(platform, user_id, msg)
                    clear_user_history(user_key)
                    show_menu(platform, user_id, user_key)
                    cache_set(user_state, user_key, 'waiting_choice')
                except Exception as e:
                    log_error(e)
                    send_msg(platform, user_id, f"Помилка: {str(e)}")
                return

        if state == 'waiting_address':
            data = cache_get(user_data, user_key)
            data['address'] = text
            cache_set(user_data, user_key, data)
            try:
                order_id, discount, ref_code = create_order(
                    user_key, platform, data['device'], data['description'],
                    data['phone'], data['address'], data['service_type'], data.get('used_referral')
                )
                msg = t(lang, 'order_accepted', order_id=order_id)
                if discount:
                    msg += t(lang, 'your_discount', discount=discount)
                msg += t(lang, 'your_ref', ref_code=ref_code)
                msg += t(lang, 'master_contact')
                send_msg(platform, user_id, msg)
                clear_user_history(user_key)
                show_menu(platform, user_id, user_key)
                cache_set(user_state, user_key, 'waiting_choice')
            except Exception as e:
                log_error(e)
                send_msg(platform, user_id, f"Помилка: {str(e)}")
            return

        send_msg(platform, user_id, t(lang, 'not_understand'))
        
    except Exception as e:
        log_error(e)
        try:
            send_msg(platform, user_id, f"Критична помилка: {str(e)}")
        except:
            pass