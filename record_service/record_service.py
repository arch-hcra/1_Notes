import os
import json
from flask import Flask, request, jsonify

app = Flask(__name__)
FILENAME = 'records.json'

def save_record(text):
    records = read_records()
    records.append(text)
    with open(FILENAME, 'w') as file:
        json.dump(records, file)

def read_records():
    if not os.path.exists(FILENAME):
        return []
    try:
        with open(FILENAME, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []

def delete_record(text):
    records = read_records()
    records = [record for record in records if record != text]
    with open(FILENAME, 'w') as file:
        json.dump(records, file)

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

