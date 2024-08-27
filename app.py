import os
import sqlite3
from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Use an absolute path to the database
BASE_DIR = os.path.dirname(__file__)
DATABASE = os.path.join(BASE_DIR, 'data/light_data.db')

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS light_status (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        status TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT status, timestamp FROM light_status ORDER BY timestamp DESC')
    rows = cursor.fetchall()
    conn.close()
    return render_template('index.html', rows=rows)

@app.route('/api/ldr', methods=['POST'])
def ldr_data():
    status = request.form['status']
    timestamp = datetime.now()

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO light_status (status, timestamp) VALUES (?, ?)', (status, timestamp))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Data stored successfully', 'status': status, 'timestamp': timestamp})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
