from flask import Blueprint, request, Response, abort
import os
import json
import sqlite3
import csv
import io

admin_bp = Blueprint('admin', __name__)
ADMIN_IDS = os.getenv('ADMIN_IDS', '5006092089').split(',')
DB_PATH = '/home/smertnik/bot/bot.db'

def check_admin():
    token = request.args.get('token')
    if not token or str(token) not in ADMIN_IDS:
        abort(403)
    return True

@admin_bp.route('/admin')
def admin_panel():
    check_admin()
    token = request.args.get('token')
    html = f'''
    <html>
    <head><meta charset="utf-8"><title>Admin Panel</title></head>
    <body>
    <h2>🔧 Admin Panel</h2>
    <p><a href="/admin/export?token={token}">📥 Скачать заказы CSV</a></p>
    <p><a href="/admin/stats?token={token}">📊 Скачать статистику CSV</a></p>
    <p><a href="/admin/orders?token={token}">📋 Смотреть все заказы JSON</a></p>
    </body>
    </html>
    '''
    return html

@admin_bp.route('/admin/export')
def admin_export():
    check_admin()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('SELECT * FROM orders ORDER BY created DESC')
        rows = c.fetchall()
        cols = [desc[0] for desc in c.description]
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(cols)
        writer.writerows(rows)
        csv_data = output.getvalue()
        output.close()
        
        return Response(
            csv_data,
            mimetype='text/csv; charset=utf-8',
            headers={'Content-Disposition': 'attachment;filename=orders.csv'}
        )
    except Exception as e:
        return f"Помилка: {str(e)}", 500
    finally:
        conn.close()

@admin_bp.route('/admin/stats')
def admin_stats():
    check_admin()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('''SELECT device, COUNT(*) as count, SUM(discount) as total_discount 
                     FROM orders GROUP BY device ORDER BY count DESC''')
        rows = c.fetchall()
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['device', 'count', 'total_discount'])
        writer.writerows(rows)
        csv_data = output.getvalue()
        output.close()
        
        return Response(
            csv_data,
            mimetype='text/csv; charset=utf-8',
            headers={'Content-Disposition': 'attachment;filename=stats.csv'}
        )
    except Exception as e:
        return f"Помилка: {str(e)}", 500
    finally:
        conn.close()

@admin_bp.route('/admin/orders')
def admin_orders():
    check_admin()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('SELECT * FROM orders ORDER BY created DESC LIMIT 100')
        rows = c.fetchall()
        cols = [desc[0] for desc in c.description]
        result = [dict(zip(cols, row)) for row in rows]
        return Response(json.dumps(result, ensure_ascii=False, indent=2), mimetype='application/json')
    except Exception as e:
        return f"Помилка: {str(e)}", 500
    finally:
        conn.close()