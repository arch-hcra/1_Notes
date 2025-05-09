from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = 'd39xu42'


FILE_SERVICE_URL = 'http://file_service:5001'
DB_SERVICE_URL = 'http://display_service:5002'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/view_records')
def view_records():
    response = requests.get(f'{FILE_SERVICE_URL}/records')
    records = response.json().get('records', [])
    return render_template('records.html', records=records)

@app.route('/view_db_records')
def view_db_records():
    response = requests.get(f'{DB_SERVICE_URL}/records')
    db_records = response.json().get('records', [])
    return render_template('db_records.html', records=db_records)

@app.route('/add', methods=['POST'])
def add_record():
    text = request.form.get('text')
    if text and text.strip():
        response = requests.post(f'{FILE_SERVICE_URL}/add', data={'text': text})
        if response.json().get('success'):
            flash('Added successfully.', 'success')
        else:
            flash('Failed to add record.', 'error')
    return redirect(url_for('index'))

@app.route('/delete/<record>', methods=['POST'])
def delete_record(record):
    response = requests.post(f'{FILE_SERVICE_URL}/delete', json={'data': record})
    if response.json().get('success'):
        flash('Successfully deleted.', 'success')
    else:
        flash('Failed to delete.', 'error')
    return redirect(url_for('view_records'))

@app.route('/delete_db_record/<record>', methods=['POST'])
def delete_db_record(record):
    response = requests.post(f'{DB_SERVICE_URL}/delete', json={'text': record})
    if response.json().get('success'):
        flash('Been successfully deleted from the database.', 'success')
    else:
        flash('Failed to delete record from database.', 'error')
    return redirect(url_for('view_db_records'))

@app.route('/upload_to_db', methods=['POST'])
def upload_to_db():
    file_records_response = requests.get(f'{FILE_SERVICE_URL}/records')
    file_records = file_records_response.json().get('records', [])

    existing_records_response = requests.get(f'{DB_SERVICE_URL}/records')
    existing_records = existing_records_response.json().get('records', [])
    existing_records_set = set(existing_records)

    for record in file_records:
        if record not in existing_records_set:
            requests.post(f'{DB_SERVICE_URL}/write', json={'data': record})

    flash('Date is recods in database.', 'success')
    return redirect(url_for('view_records'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
