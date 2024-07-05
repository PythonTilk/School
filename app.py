from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('tips.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            team TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['username']
    team = request.form['team']
    conn = sqlite3.connect('tips.db')
    c = conn.cursor()
    c.execute('INSERT INTO tips (username, team) VALUES (?, ?)', (username, team))
    conn.commit()
    conn.close()
    return redirect(url_for('results'))

@app.route('/results')
def results():
    conn = sqlite3.connect('tips.db')
    c = conn.cursor()
    c.execute('SELECT username, team FROM tips')
    tips = c.fetchall()
    conn.close()
    return render_template('results.html', tips=tips)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
