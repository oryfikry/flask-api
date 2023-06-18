from flask import Flask, jsonify, request
import sqlite3
from datetime import date

app = Flask(__name__)
DATABASE = 'database.db'

# Function to create the database table
def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        '''
    )
    conn.commit()
    conn.close()

# Create the table when the application starts
create_table()

# Function to create a new item
def create_item(code):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO items (code, created_at) VALUES (?, datetime("now"))', (code,))
    conn.commit()
    item_id = cursor.lastrowid
    conn.close()
    return item_id

# Route to create a new item
@app.route('/items', methods=['POST'])
def create():
    if 'code' not in request.json:
        return jsonify({'error': 'Code is required'}), 400
    code = request.json['code']
    item_id = create_item(code)
    return jsonify({'id': item_id}), 201

# Function to get an item by ID
def get_item_by_id(item_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items WHERE code = ?', (item_id,))
    item = cursor.fetchone()
    conn.close()
    if item:
        return {
            'id': item[0],
            'code': item[1],
            'created_at': item[2]
        }
    return None

# Route to get an item by ID
@app.route('/items/<string:item_id>', methods=['GET'])
def get_item(item_id):
    item = get_item_by_id(str(item_id))
    if item:
        return jsonify(item), 200
    return jsonify({'error': 'Item not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
