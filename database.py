import sqlite3
import os

# Render дозволяє писати в /opt/render/project/src
DB_PATH = os.path.join(os.path.dirname(__file__), 'bot.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (platform TEXT, user_id TEXT, lang TEXT, PRIMARY KEY (platform, user_id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS orders
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  platform TEXT,
                  user_id TEXT,
                  device TEXT,
                  service_type TEXT,
                  description TEXT,
                  photos TEXT,
                  contact TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def get_user_lang(platform, user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT lang FROM users WHERE platform=? AND user_id=?', (platform, str(user_id)))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def set_user_lang(platform, user_id, lang):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO users (platform, user_id, lang) VALUES (?,?,?)', 
              (platform, str(user_id), lang))
    conn.commit()
    conn.close()

def save_order(platform, user_id, device, service_type, description, photos, contact):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO orders (platform, user_id, device, service_type, description, photos, contact)
                 VALUES (?,?,?,?,?,?,?)''',
              (platform, str(user_id), device, service_type, description, str(photos), contact))
    order_id = c.lastrowid
    conn.commit()
    conn.close()
    return order_id

def get_order(order_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM orders WHERE id=?', (order_id,))
    row = c.fetchone()
    conn.close()
    return row
