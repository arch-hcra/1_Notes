from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_record():
    text = request.form.get('text')
    if text:
        save_record(text)
    return redirect(url_for('view_records'))

@app.route('/records')
def view_records():
    records = read_records()
    return render_template('records.html', records=records)

if __name__ == '__main__':
    app.run(debug=True)
