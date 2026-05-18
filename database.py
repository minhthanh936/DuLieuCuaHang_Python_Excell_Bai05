import sqlite3

def init_db():
    conn = sqlite3.connect('store_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id TEXT PRIMARY KEY,
            name TEXT,
            quantity INTEGER,
            price REAL,
            total REAL,
            note TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_all_items():
    conn = sqlite3.connect('store_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM inventory')
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_item(item_id, name, qty, price, total, note):
    conn = sqlite3.connect('store_data.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO inventory VALUES (?,?,?,?,?,?)', 
                       (item_id, name, qty, price, total, note))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def update_item(item_id, name, qty, price, total, note):
    conn = sqlite3.connect('store_data.db')
    cursor = conn.cursor()
    cursor.execute('''UPDATE inventory SET name=?, quantity=?, price=?, total=?, note=? 
                      WHERE id=?''', (name, qty, price, total, note, item_id))
    conn.commit()
    conn.close()

def delete_item(item_id):
    conn = sqlite3.connect('store_data.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM inventory WHERE id=?', (item_id,))
    conn.commit()
    conn.close()

def clear_all():
    conn = sqlite3.connect('store_data.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM inventory')
    conn.commit()
    conn.close()