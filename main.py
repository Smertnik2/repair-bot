from flask import Flask, request, jsonify
from config import TG_BOT_TOKEN, FB_VERIFY_TOKEN
from handlers import handle_message, handle_start, processed_callbacks, tg_answer_callback
from database import init_db, update_order_status
from texts import t
from ui import send_text

app = Flask(__name__)

@app.route('/')
def index():
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
            
            tg_answer_callback(cb_id)
            handle_message('tg', user_id, '', callback_data=cb_data)
            return jsonify({'ok': True})
        
        if 'message' in data:
            msg = data['message']
            user_id = msg['from']['id']
            text = msg.get('text', '')
            message_id = msg['message_id']
            photo = msg['photo'][-1]['file_id'] if 'photo' in msg else None
            
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
        return 'Verification failed', 403
    
    data = request.json
    try:
        for entry in data.get('entry', []):
            for messaging in entry.get('messaging', []):
                sender_id = messaging['sender']['id']
                
                if 'message' in messaging:
                    msg = messaging['message']
                    text = msg.get('text', '')
                    
                    # Quick reply payload
                    if 'quick_reply' in msg:
                        text = msg['quick_reply']['payload']
                    
                    handle_message('fb', sender_id, text)
                
                elif 'postback' in messaging:
                    payload = messaging['postback']['payload']
                    handle_message('fb', sender_id, '', callback_data=payload)
    except Exception as e:
        print(f'FB webhook error: {e}')
    
    return 'OK', 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
