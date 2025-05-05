import requests
from flask import Flask, render_template, request, redirect, url_for, flash

# Пример запроса к record_service
RECORD_SERVICE_URL = 'http://record_service:5000'  # Имя сервиса из docker-compose.yml

def save_record(text):
    requests.post(f"{RECORD_SERVICE_URL}/save", json={"text": text})

def read_records():
    response = requests.get(f"{RECORD_SERVICE_URL}/records")
    return response.json() if response.status_code == 200 else []

app = Flask(__name__)
app.secret_key = 'd79x234'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_record_route():
    text = request.form.get('text', '').strip()
    if text:
        save_record(text)
        flash('Successfully added', 'success')
    else:
        flash('Text cannot be empty.', 'error')
    return redirect(url_for('view_records'))

@app.route('/records')
def view_records():
    records = read_records()
    return render_template('records.html', records=records)

@app.route('/delete', methods=['POST'])
def delete_record_route():
    text = request.form.get('text', '').strip()
    if text:
        requests.post(f"{RECORD_SERVICE_URL}/delete", json={"text": text})
        flash('Successfully deleted', 'success')
    return redirect(url_for('view_records'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
