from flask import Blueprint
from config import ADMIN_IDS, DB_PATH
from ui import send_text
from texts import t
import sqlite3

admin_bp = Blueprint('admin', __name__)

def is_admin(user_id):
    return str(user_id) in ADMIN_IDS

def get_admin_lang(user_id):
    # Админка пока на русском, но можно вынести в переменную
    return 'ru'

@admin_bp.route('/admin/stats')
def admin_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM orders')
    total = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM orders WHERE status="new"')
    new = c.fetchone()[0]
    conn.close()
    return f'Total: {total}, New: {new}'

def notify_admins_new_order(order_id, order_data):
    lang = 'ru'  # админы получают на русском
    msg = f"<b>🔔 Новая заявка #{order_id}</b>\n\n"
    msg += f"📱 {order_data['device']}\n"
    msg += f"🏷 {order_data['brand']}\n"
    msg += f"🔧 {order_data['problem']}\n"
    msg += f"📞 {order_data['phone']}\n"
    msg += f"👤 {order_data['name']}\n"
    msg += f"Platform: {order_data['platform']}"
    
    for admin_id in ADMIN_IDS:
        send_text('tg', admin_id, msg, parse_mode='HTML')
