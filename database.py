import sqlite3
import random
import string
from datetime import datetime

DB_PATH = '/home/smertnik/bot/bot.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_key TEXT,
        platform TEXT,
        device TEXT,
        description TEXT,
        phone TEXT,
        address TEXT,
        service_type TEXT,
        status TEXT DEFAULT 'Нове',
        discount INTEGER DEFAULT 0,
        ref_code TEXT,
        used_referral TEXT,
        created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('CREATE TABLE IF NOT EXISTS processed_msgs (msg_id INTEGER PRIMARY KEY)')
    conn.commit()
    conn.close()

def generate_ref_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def create_order(user_key, platform, device, description, phone, address, service_type, used_referral=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    ref_code = generate_ref_code()
    discount = 0

    if used_referral:
        c.execute('SELECT id FROM orders WHERE ref_code =?', (used_referral,))
        if c.fetchone():
            discount = 10

    c.execute('SELECT COUNT(*) FROM orders WHERE user_key =? AND status = "Готово"', (user_key,))
    if c.fetchone()[0] > 0:
        discount = max(discount, 5)

    c.execute('''INSERT INTO orders 
        (user_key, platform, device, description, phone, address, service_type, discount, ref_code, used_referral) 
        VALUES (?,?,?,?,?,?,?,?,?,?)''',
        (user_key, platform, device, description, phone, address, service_type, discount, ref_code, used_referral))

    order_id = c.lastrowid
    conn.commit()
    conn.close()
    return order_id, discount, ref_code

def get_user_orders(user_key):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''SELECT id, device, status, discount, created FROM orders 
                 WHERE user_key =? ORDER BY created DESC LIMIT 10''', (user_key,))
    rows = c.fetchall()
    conn.close()
    return rows

def update_order_status(order_id, status):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('UPDATE orders SET status =? WHERE id =?', (status, order_id))
    conn.commit()
    conn.close()

def is_loyal_client(user_key):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM orders WHERE user_key =? AND status = "Готово"', (user_key,))
    count = c.fetchone()[0]
    conn.close()
    return count > 0