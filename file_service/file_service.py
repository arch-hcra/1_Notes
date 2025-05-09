from flask import Flask, request, jsonify, flash

app = Flask(__name__)
app.secret_key = 'd79x234'

def save_record(text):
    with open('records.txt', 'a') as file:
        file.write(text + '\n')

def read_records():
    try:
        with open('records.txt', 'r') as file:
            return [record.strip() for record in file]
    except FileNotFoundError:
        return []

def delete_record_from_file(text):
    records = read_records()
    records = [record for record in records if record != text]
    with open('records.txt', 'w') as file:
        file.writelines(record + '\n' for record in records)

@app.route('/add', methods=['POST'])
def add_record():
    text = request.form.get('text')
    if text and text.strip():
        save_record(text)
        flash('Record successfully added to the text file.', 'success')
    else:
        flash('Field cannot be empty.', 'error')
    return jsonify(success=True)

@app.route('/records', methods=['GET'])
def view_records():
    records = read_records()
    return jsonify(records=records)

@app.route('/delete', methods=['POST'])
def delete_record():
    data = request.json
    text = data.get('data') 
    if text:
        delete_record_from_file(text)
        flash('Record successfully deleted from the text file.', 'success')
        return jsonify(success=True)
    return jsonify(success=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
