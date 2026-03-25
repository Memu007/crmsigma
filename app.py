import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from urllib.parse import urlparse

app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app)

# Configuration for Database
# Railway provides DATABASE_URL. If running locally without it, fallback to SQLite.
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

if not database_url:
    # Ensure data directory exists for local testing
    os.makedirs(os.path.join(app.root_path, 'data'), exist_ok=True)
    database_url = f"sqlite:///{os.path.join(app.root_path, 'data', 'database.db')}"

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class AppData(db.Model):
    __tablename__ = 'app_data'
    id = db.Column(db.Integer, primary_key=True)
    # Storing the entire JSON payload in a single row
    data = db.Column(db.JSON, nullable=False)

def init_db():
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if database is empty
        record = AppData.query.first()
        if not record:
            # Check if there is a local database.json to migrate
            old_db_path = os.path.join(app.root_path, 'data', 'database.json')
            if os.path.exists(old_db_path):
                print(f"Migrating existing data from {old_db_path} to database...")
                with open(old_db_path, 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError:
                        data = {"clientes":[], "contactos":[], "visitas":[], "meta":{}}
            else:
                print("Initializing empty database...")
                data = {"clientes":[], "contactos":[], "visitas":[], "meta":{}}
            
            # Insert initial data
            new_record = AppData(id=1, data=data)
            db.session.add(new_record)
            db.session.commit()
            print("Database initialized successfully.")

# Main index redirect
@app.route('/')
def index():
    return send_from_directory('.', 'programa.html')

# API Endpoints matching previous server.py
@app.route('/api/data', methods=['GET'])
def get_data():
    record = AppData.query.first()
    if record and record.data:
        return jsonify(record.data)
    return jsonify({"clientes":[], "contactos":[], "visitas":[], "meta":{}})

@app.route('/api/data', methods=['POST'])
def save_data():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid or missing JSON"}), 400
            
        record = AppData.query.first()
        if record:
            record.data = data
        else:
            record = AppData(id=1, data=data)
            db.session.add(record)
            
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Keep the backup endpoint to return empty to not break the frontend if it's there
@app.route('/api/backups', methods=['GET'])
def get_backups():
    # Backups managed by Railway database now, returning empty list
    return jsonify([])

@app.route('/api/backup', methods=['POST'])
def create_backup():
    return jsonify({"success": True, "message": "Backups are automatically managed by the database."})

# Catch-all for static files
@app.route('/<path:path>')
def send_static(path):
    return send_from_directory('.', path)

# Initialize database
init_db()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f"Server starting on port {port}...")
    app.run(host='0.0.0.0', port=port)
