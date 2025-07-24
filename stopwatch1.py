from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session

@app.route('/')
def index():
    elapsed = None
    if 'start_time' in session:
        if session.get('running', False):
            elapsed = time.time() - session['start_time']
        else:
            elapsed = session.get('elapsed', 0)
    return render_template('index.html', elapsed=elapsed)

@app.route('/start', methods=['POST'])
def start():
    if not session.get('running', False):
        session['start_time'] = time.time() - session.get('elapsed', 0)
        session['running'] = True
    return redirect(url_for('index'))

@app.route('/stop', methods=['POST'])
def stop():
    if session.get('running', False):
        session['elapsed'] = time.time() - session['start_time']
        session['running'] = False
    return redirect(url_for('index'))

@app.route('/reset', methods=['POST'])
def reset():
    session.pop('start_time', None)
    session['elapsed'] = 0
    session['running'] = False
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

