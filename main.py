from flask import Flask, request, jsonify
import requests
from config import *
from handlers import (
    handle_message, processing_users, processed_callbacks, user_lang,
    cache_get, cache_set
)
from database import update_order_status, init_db
from texts import STATUS_TRANS, t
from keyboards import send_msg, tg_send
from admin import admin_bp

app = Flask(__name__)
app.register_blueprint(admin_bp)

# init_db() ПРИБРАВ ЗВІДСИ

@app.route('/')
def index():
    # Створюємо БД при першому заході на головну
    try:
        init_db()
    except Exception as e:
        print(f'DB init error: {e}')
    return 'Bot is running!'

@app.route('/tg_webhook', methods=['POST'])
def tg_webhook():
    try:
        data = request.json
        
        if 'callback_query' in data:
            cb = data['callback_query']
            cb_id = cb['id']
            user_id = cb['from']['id']
            cb_data = cb['data']
            
            if cb_id in processed_callbacks:
                return jsonify({'ok': True})
            processed_callbacks.add(cb_id)
            
            requests.post(f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/answerCallbackQuery',
                         json={'callback_query_id': cb_id})
            
            if cb_data.startswith('STATUS_'):
                parts = cb_data.split('_')
                if len(parts) == 3:
                    new_status, order_id = parts[1], parts[2]
                    lang = cache_get(user_lang, f'tg_{user_id}', 'ua')
                    status_text = STATUS_TRANS.get(new_status, {}).get(lang, new_status)
                    try:
                        update_order_status(order_id, new_status)
                        tg_send(user_id, t(lang, 'order_status_updated', order_id=order_id, status=status_text))
                    except Exception as e:
                        tg_send(user_id, f"Помилка: {str(e)}")
            
            handle_message('tg', user_id, cb_data, message_id=cb['message']['message_id'])
            return jsonify({'ok': True})
        
        if 'message' in data:
            msg = data['message']
            user_id = msg['from']['id']
            text = msg.get('text', '')
            message_id = msg['message_id']
            photo = None
            
            if 'photo' in msg:
                photo = msg['photo'][-1]['file_id']
            
            handle_message('tg', user_id, text, message_id=message_id, photo=photo)
            return jsonify({'ok': True})
            
    except Exception as e:
        print(f'TG webhook error: {e}')
        return jsonify({'ok': True})
    
    return jsonify({'ok': True})

@app.route('/fb_webhook', methods=['GET', 'POST'])
def fb_webhook():
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == FB_VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        return 'Verification token mismatch', 403
    
    if request.method == 'POST':
        data = request.json
        try:
            for entry in data.get('entry', []):
                for messaging in entry.get('messaging', []):
                    sender_id = messaging['sender']['id']
                    
                    if 'message' in messaging and 'text' in messaging['message']:
                        text = messaging['message']['text']
                        handle_message('fb', sender_id, text)
                    
                    if 'message' in messaging and 'attachments' in messaging['message']:
                        for attach in messaging['message']['attachments']:
                            if attach['type'] == 'image':
                                photo_url = attach['payload']['url']
                                handle_message('fb', sender_id, '', photo=photo_url)
                    
                    if 'postback' in messaging:
                        payload = messaging['postback']['payload']
                        handle_message('fb', sender_id, payload)
                        
        except Exception as e:
            print(f'FB webhook error: {e}')
        
        return 'OK', 200

if __name__ == '__main__':
    app.run(debug=True)