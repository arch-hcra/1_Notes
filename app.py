from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2

app = Flask(__name__)
app.secret_key = 'd79x234'


DB_CONFIG = {
    'dbname': 'test',
    'user': 'postgres',
    'password': 'postgres',
    'host': '192.168.0.107',
    'port': '5432'
}

def create_connection():
    return psycopg2.connect(**DB_CONFIG)

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

def delete_record_from_file(text):
    records = read_records()
    records = [record for record in records if record != text]
    with open('records.txt', 'w') as file:
        for record in records:
            file.write(record + '\n')

def write_to_db(data):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO text (ins) VALUES (%s)", (data,))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error writing to database: {e}")

def get_records_from_db():
    records = []
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ins FROM text")
        rows = cursor.fetchall()
        for row in rows:
            records.append(row[0])
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error retrieving records from database: {e}")
    return records

def delete_record_from_db(text):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM text WHERE ins = %s", (text,))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error deleting record from database: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_record():
    text = request.form.get('text')
    if text and text.strip():
        save_record(text) 
        flash('Record successfully added to the text file.', 'success')
    else:
        flash('Field cannot be empty.', 'error')
    return redirect(url_for('view_records'))

@app.route('/records')
def view_records():
    records = read_records()
    return render_template('records.html', records=records)

@app.route('/delete_from_file', methods=['POST'])
def delete_record_from_file_route():
    text = request.form.get('text')
    if text:
        delete_record_from_file(text) 
        flash('Record successfully deleted from the text file.', 'success')
    return redirect(url_for('view_records'))

@app.route('/delete_from_db', methods=['POST'])
def delete_record_from_db_route():
    text = request.form.get('text')
    if text:
        delete_record_from_db(text)
        flash('Record successfully deleted from the database.', 'success')
    return redirect(url_for('view_db_records'))

@app.route('/upload_to_db', methods=['POST'])
def upload_to_db():
    records = read_records()
    existing_records = get_records_from_db()  

    for record in records:
        if record not in existing_records: 
            write_to_db(record)
    
    flash('All new records successfully uploaded to the database.', 'success')
    return redirect(url_for('view_records'))

@app.route('/view_db_records')
def view_db_records():
    records = get_records_from_db() 
    return render_template('db_records.html', records=records)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
