import os
import json
import sqlite3
import psycopg2
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app)

database_url = os.environ.get('DATABASE_URL')

def get_db_connection():
    if database_url:
        # Postgres connection
        conn = psycopg2.connect(database_url)
        return conn, 'postgres'
    else:
        # SQLite local fallback
        os.makedirs(os.path.join(app.root_path, 'data'), exist_ok=True)
        db_path = os.path.join(app.root_path, 'data', 'database.db')
        conn = sqlite3.connect(db_path)
        return conn, 'sqlite'

def init_db():
    conn, db_type = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if db_type == 'postgres':
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS app_data (
                    id INTEGER PRIMARY KEY,
                    data JSONB NOT NULL
                )
            """)
        else:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS app_data (
                    id INTEGER PRIMARY KEY,
                    data TEXT NOT NULL
                )
            """)
        
        # Check if database is empty
        cursor.execute("SELECT data FROM app_data WHERE id = 1")
        record = cursor.fetchone()
        
        if not record:
            data = {"clientes":[], "contactos":[], "visitas":[], "meta":{}}
            # Migrate local database.json if exists
            old_db_path = os.path.join(app.root_path, 'data', 'database.json')
            if os.path.exists(old_db_path):
                print(f"Migrating existing data from {old_db_path}...")
                with open(old_db_path, 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError:
                        pass
            
            # Insert initial data
            if db_type == 'postgres':
                cursor.execute("INSERT INTO app_data (id, data) VALUES (1, %s)", (json.dumps(data),))
            else:
                cursor.execute("INSERT INTO app_data (id, data) VALUES (1, ?)", (json.dumps(data),))
            
            conn.commit()
            print("Database initialized successfully.")
    finally:
        cursor.close()
        conn.close()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    conn, db_type = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT data FROM app_data WHERE id = 1")
        record = cursor.fetchone()
        
        if record:
            raw_data = record[0]
            if isinstance(raw_data, dict):
                return jsonify(raw_data)
            return jsonify(json.loads(raw_data))
            
    except Exception as e:
        print("Error reading database:", e)
    finally:
        cursor.close()
        conn.close()
        
    return jsonify({"clientes":[], "contactos":[], "visitas":[], "meta":{}})

@app.route('/api/data', methods=['POST'])
def save_data():
    conn, db_type = get_db_connection()
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid or missing JSON"}), 400
            
        cursor = conn.cursor()
        
        if db_type == 'postgres':
            cursor.execute("UPDATE app_data SET data = %s WHERE id = 1", (json.dumps(data),))
            if cursor.rowcount == 0:
                cursor.execute("INSERT INTO app_data (id, data) VALUES (1, %s)", (json.dumps(data),))
        else:
            cursor.execute("UPDATE app_data SET data = ? WHERE id = 1", (json.dumps(data),))
            if cursor.rowcount == 0:
                cursor.execute("INSERT INTO app_data (id, data) VALUES (1, ?)", (json.dumps(data),))
                
        conn.commit()
        return jsonify({"success": True})
    except Exception as e:
        conn.rollback()
        print("Error saving database:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/backups', methods=['GET'])
def get_backups():
    return jsonify([])

@app.route('/api/backup', methods=['POST'])
def create_backup():
    return jsonify({"success": True, "message": "Backups are automatically managed by the database."})

@app.route('/<path:path>')
def send_static(path):
    return send_from_directory('.', path)

# Only initialize DB locally safely, Railway config allows this block to run fine.
try:
    init_db()
except Exception as e:
    print("Database init warning (ok if first run):", e)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f"Server starting on port {port}...")
    app.run(host='0.0.0.0', port=port)
