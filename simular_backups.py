#!/usr/bin/env python3
"""
Script para simular 6 meses de backups
Crea copias del database.json con fechas de julio a diciembre 2025
"""

import json
import os
import shutil
from datetime import datetime

BACKUP_DIR = "data/backups"
DATABASE_FILE = "data/database.json"

# Fechas de backups simulados (fin de cada mes)
FECHAS_BACKUP = [
    "2025-07-31",
    "2025-08-31",
    "2025-09-30",
    "2025-10-31",
    "2025-11-30",
    "2025-12-15"  # Último backup (hoy)
]

def main():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    # Leer datos actuales
    with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for fecha in FECHAS_BACKUP:
        backup_name = f"backup_{fecha}.json"
        backup_path = os.path.join(BACKUP_DIR, backup_name)
        
        # Crear backup con metadata de fecha
        backup_data = {
            "_backup_info": {
                "fecha": fecha,
                "creado": datetime.now().isoformat(),
                "clientes": len(data.get('clientes', [])),
                "visitas": len(data.get('visitas', [])),
                "contactos": len(data.get('contactos', []))
            },
            **data
        }
        
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Backup creado: {backup_name}")
    
    print(f"\n📁 Backups en: {BACKUP_DIR}/")
    print(f"   Total: {len(FECHAS_BACKUP)} backups")

if __name__ == "__main__":
    main()
