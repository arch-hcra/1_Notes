import os
from flask import Flask, request, jsonify

app = Flask(__name__)
FILENAME = 'records.txt'

def save_record(text):
    with open(FILENAME, 'a') as file:
        file.write(text + '\n')

def read_records():
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, 'r') as file:
        return [record.strip() for record in file.readlines()]

def delete_record(text):
    records = read_records()
    records = [record for record in records if record != text]
    with open(FILENAME, 'w') as file:
        file.writelines(record + '\n' for record in records)

@app.route('/save', methods=['POST'])
def save_record_route():
    data = request.get_json()
    save_record(data['text'])
    return '', 204

@app.route('/records', methods=['GET'])
def get_records():
    records = read_records()
    return jsonify(records)

@app.route('/delete', methods=['POST'])
def delete_record_route():
    data = request.get_json()
    delete_record(data['text'])
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
