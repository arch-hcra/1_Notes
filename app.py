from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'd79x234'

def save_record(text):
    with open('records.txt', 'a') as file:
        file.write(text + '\n') 

def read_records():
    try:
        with open('records.txt', 'r') as file:
            records = file.readlines()
        return [record.strip() for record in records]
    except FileNotFoundError:
        return []

def delete_record(text):
    records = read_records()
    records = [record for record in records if record != text]
    with open('records.txt', 'w') as file:
        for record in records:
            file.write(record + '\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_record():
    text = request.form.get('text')
    if text and text.strip():
        save_record(text)
        flash('Success add', 'success')
    else:
        flash('Is not is empty.', 'error')
    return redirect(url_for('view_records'))

@app.route('/records')
def view_records():
    records = read_records()
    return render_template('records.html', records=records)

@app.route('/delete', methods=['POST'])
def delete_record_route():
    text = request.form.get('text')
    if text:
        delete_record(text)
        flash('Deleted success', 'success')
    return redirect(url_for('view_records'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
