#!/usr/bin/env python3
"""
Servidor para SigmaLine CRM con persistencia en JSON
- Backups automáticos cada 30 días
Ejecutar: python3 server.py
Acceder: http://localhost:8000
"""

import http.server
import socketserver
import webbrowser
import os
import json
import shutil
from datetime import datetime, timedelta

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
DATABASE_FILE = os.path.join(DIRECTORY, 'data', 'database.json')
BACKUP_DIR = os.path.join(DIRECTORY, 'data', 'backups')
BACKUP_INTERVAL_DAYS = 30

def check_and_create_backup():
    """Crea backup automático si pasaron 30 días desde el último"""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    if not os.path.exists(DATABASE_FILE):
        return
    
    # Buscar último backup
    backups = sorted([f for f in os.listdir(BACKUP_DIR) if f.startswith('backup_') and f.endswith('.json')])
    
    should_backup = False
    if not backups:
        should_backup = True
        print("📁 No hay backups previos, creando primero...")
    else:
        # Obtener fecha del último backup del nombre del archivo
        last_backup = backups[-1]
        try:
            # Formato: backup_YYYY-MM-DD.json
            date_str = last_backup.replace('backup_', '').replace('.json', '')
            last_date = datetime.strptime(date_str, '%Y-%m-%d')
            days_since = (datetime.now() - last_date).days
            
            if days_since >= BACKUP_INTERVAL_DAYS:
                should_backup = True
                print(f"📁 Último backup hace {days_since} días, creando nuevo...")
        except:
            should_backup = True
    
    if should_backup:
        create_backup()

def create_backup():
    """Crea un backup del database.json actual"""
    if not os.path.exists(DATABASE_FILE):
        return
    
    today = datetime.now().strftime('%Y-%m-%d')
    backup_name = f"backup_{today}.json"
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    
    # Si ya existe backup de hoy, no duplicar
    if os.path.exists(backup_path):
        print(f"✅ Backup de hoy ya existe: {backup_name}")
        return
    
    try:
        # Leer datos actuales y agregar metadata
        with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        backup_data = {
            "_backup_info": {
                "fecha": today,
                "creado": datetime.now().isoformat(),
                "clientes": len(data.get('clientes', [])),
                "visitas": len(data.get('visitas', [])),
                "contactos": len(data.get('contactos', []))
            },
            **data
        }
        
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Backup automático creado: {backup_name}")
    except Exception as e:
        print(f"❌ Error creando backup: {e}")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def do_GET(self):
        # Redirigir / a programa.html
        if self.path == '/':
            self.path = '/programa.html'
        
        # API: Leer base de datos
        if self.path == '/api/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            try:
                with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
                    data = f.read()
                self.wfile.write(data.encode('utf-8'))
            except FileNotFoundError:
                self.wfile.write(b'{"clientes":[],"contactos":[],"visitas":[],"meta":{}}')
            return
        
        # API: Listar backups
        if self.path == '/api/backups':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            backups = []
            if os.path.exists(BACKUP_DIR):
                for f in sorted(os.listdir(BACKUP_DIR), reverse=True):
                    if f.startswith('backup_') and f.endswith('.json'):
                        path = os.path.join(BACKUP_DIR, f)
                        size = os.path.getsize(path)
                        backups.append({"name": f, "size": size})
            
            self.wfile.write(json.dumps(backups).encode('utf-8'))
            return
        
        return super().do_GET()
    
    def do_POST(self):
        # API: Guardar base de datos
        if self.path == '/api/data':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Validar que sea JSON válido
                data = json.loads(post_data.decode('utf-8'))
                
                # Guardar al archivo
                os.makedirs(os.path.dirname(DATABASE_FILE), exist_ok=True)
                with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(b'{"success": true}')
                print(f"💾 Datos guardados en {DATABASE_FILE}")
            except json.JSONDecodeError as e:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(f'{{"error": "JSON inválido: {str(e)}"}}'.encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(f'{{"error": "{str(e)}"}}'.encode())
            return
        
        # API: Crear backup manual
        if self.path == '/api/backup':
            create_backup()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'{"success": true}')
            return
        
        return super().do_POST()
    
    def do_OPTIONS(self):
        # CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == "__main__":
    os.chdir(DIRECTORY)
    
    # Verificar que existe el archivo de datos
    if os.path.exists(DATABASE_FILE):
        print(f"📂 Base de datos: {DATABASE_FILE}")
    else:
        print(f"⚠️  Base de datos no encontrada, se creará al guardar")
    
    # Verificar y crear backup si es necesario
    check_and_create_backup()
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}"
        print(f"\n🚀 SigmaLine CRM Server con Persistencia")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"📍 Sirviendo: {DIRECTORY}")
        print(f"🌐 URL: {url}")
        print(f"💾 API GET/POST: {url}/api/data")
        print(f"📁 Backups: {BACKUP_DIR} (cada {BACKUP_INTERVAL_DAYS} días)")
        print(f"\n   Presiona Ctrl+C para detener\n")
        
        # Abrir navegador automáticamente
        webbrowser.open(url)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Servidor detenido")
