
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    phone TEXT,
                    service TEXT,
                    address TEXT
                )''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/request', methods=['GET', 'POST'])
def request_service():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        service = request.form['service']
        address = request.form['address']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO requests (name, phone, service, address) VALUES (?, ?, ?, ?)",
                  (name, phone, service, address))
        conn.commit()
        conn.close()
        return render_template('confirmation.html', name=name, service=service)
    return render_template('request_form.html')

if __name__ == '__main__':
    import os
    init_db()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
