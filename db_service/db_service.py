from flask import Flask, request, jsonify
import psycopg2
from contextlib import closing

app = Flask(__name__)

DB_CONFIG = {
    'dbname': '',
    'user': '',
    'password': '',
    'host': '',
    'port': '5432'
}

def create_connection():
    return psycopg2.connect(**DB_CONFIG)

def execute_db_query(query, params=None, fetch=False):
    try:
        with closing(create_connection()) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(query, params or ())
                if fetch:
                    return cursor.fetchall()
                conn.commit()
    except Exception as e:
        print(f"Database error: {e}")

@app.route('/write', methods=['POST'])
def write_to_db():
    data = request.json.get('data')
    execute_db_query("INSERT INTO text (ins) VALUES (%s)", (data,))
    return jsonify(success=True)

@app.route('/records', methods=['GET'])
def get_records_from_db():
    records = execute_db_query("SELECT ins FROM text", fetch=True)
    return jsonify(records=[row[0] for row in records])

@app.route('/delete', methods=['POST'])
def delete_record_from_db():
    text = request.json.get('text')
    execute_db_query("DELETE FROM text WHERE ins = %s", (text,))
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
