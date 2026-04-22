from flask import Flask, request, jsonify
from handlers import handle_message, processed_callbacks
from database import init_db
import os

app = Flask(__name__)
init_db()

@app.route('/')
def home():
    return "Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    
    if 'callback_query' in data:
        callback = data['callback_query']
        callback_id = callback['id']
        
        if callback_id in processed_callbacks:
            return jsonify({'status': 'ok'})
        processed_callbacks.add(callback_id)
        
        user_id = callback['from']['id']
        data_str = callback['data']
        
        handle_admin_callback(user_id, data_str)
        return jsonify({'status': 'ok'})
    
    if 'message' not in data:
        return jsonify({'status': 'ok'})
    
    msg = data['message']
    user_id = msg['from']['id']
    message_id = msg['message_id']
    
    if 'text' in msg:
        handle_message('tg', user_id, msg['text'], message_id=message_id)
    elif 'photo' in msg:
        file_id = msg['photo'][-1]['file_id']
        caption = msg.get('caption', '')
        handle_message('tg', user_id, caption, message_id=message_id, photo=file_id)
    
    return jsonify({'status': 'ok'})

def handle_admin_callback(user_id, data):
    import sqlite3, csv, io
    from keyboards import tg_send, tg_send_document
    
    ADMIN_IDS = os.getenv('ADMIN_IDS', '5006092089').split(',')
    if str(user_id) not in ADMIN_IDS:
        tg_send(user_id, '❌ Доступ заборонено')
        return
    
    DB_PATH = '/home/smertnik/bot/bot.db'
    
    if data == 'admin_orders':
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT id, device, status, phone, created FROM orders ORDER BY created DESC LIMIT 10')
        rows = c.fetchall()
        conn.close()
        
        if not rows:
            tg_send(user_id, 'Замовлень немає')
            return
        
        msg = '<b>📋 Останні 10 замовлень:</b>\n\n'
        for oid, device, status, phone, created in rows:
            msg += f'<b>#{oid}</b> {device}\n'
            msg += f'Статус: {status}\n'
            msg += f'Телефон: {phone}\n'
            msg += f'Дата: {created[:16]}\n\n'
        tg_send(user_id, msg, parse_mode='HTML')
        
    elif data == 'admin_stats':
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM orders')
        total = c.fetchone()[0]
        c.execute('SELECT status, COUNT(*) FROM orders GROUP BY status')
        by_status = c.fetchall()
        c.execute('SELECT device, COUNT(*) FROM orders GROUP BY device ORDER BY COUNT(*) DESC LIMIT 5')
        by_device = c.fetchall()
        conn.close()
        
        msg = f'<b>📊 Статистика</b>\n\n'
        msg += f'Всього замовлень: {total}\n\n'
        msg += '<b>По статусах:</b>\n'
        for status, count in by_status:
            msg += f'{status}: {count}\n'
        msg += '\n<b>Топ пристроїв:</b>\n'
        for device, count in by_device:
            msg += f'{device}: {count}\n'
        tg_send(user_id, msg, parse_mode='HTML')
        
    elif data == 'admin_export':
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT * FROM orders ORDER BY created DESC')
        rows = c.fetchall()
        cols = [desc[0] for desc in c.description]
        conn.close()
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(cols)
        writer.writerows(rows)
        csv_data = output.getvalue()
        output.close()
        
        tg_send_document(user_id, csv_data, 'orders.csv', '📥 Всі замовлення')

if __name__ == '__main__':
    app.run(debug=True)