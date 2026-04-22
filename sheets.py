import sqlite3
import csv
from io import StringIO

def export_orders_csv():
    conn = sqlite3.connect('/home/smertnik/bot/bot.db')
    c = conn.cursor()
    try:
        c.execute('SELECT id, user_key, platform, device, description, phone, address, service_type, status, discount, ref_code, created FROM orders')
        rows = c.fetchall()
    except:
        rows = []
    conn.close()
    
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'User', 'Platform', 'Device', 'Description', 'Phone', 'Address', 'Type', 'Status', 'Discount', 'Ref', 'Created'])
    writer.writerows(rows)
    return output.getvalue()

def export_stats_csv():
    conn = sqlite3.connect('/home/smertnik/bot/bot.db')
    c = conn.cursor()
    try:
        c.execute('''
            SELECT device, COUNT(*) as count, 
                   SUM(CASE WHEN status='Готово' THEN 1 ELSE 0 END) as done,
                   SUM(CASE WHEN status='Скасовано' THEN 1 ELSE 0 END) as cancelled
            FROM orders GROUP BY device
        ''')
        rows = c.fetchall()
    except:
        rows = []
    conn.close()
    
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Device', 'Total', 'Done', 'Cancelled'])
    writer.writerows(rows)
    return output.getvalue()