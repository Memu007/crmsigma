#!/usr/bin/env python3
"""
Generador de datos demo realistas para SigmaLine CRM
- 30 clientes por vendedor (90 total)
- 4 visitas diarias por vendedor (~500 visitas en 6 meses)
- 10 prospectos nuevos por mes por vendedor
"""

import json
import random
from datetime import datetime, timedelta

# Vendedores
VENDEDORES = ['Emiliano', 'Agustina', 'Mauricio']

# Hospitales base por zona
HOSPITALES_CABA = [
    "Hospital Italiano", "Sanatorio Güemes", "Hospital Fernández", "Clínica Bazterrica",
    "Hospital Garrahan", "Sanatorio Anchorena", "Hospital Austral", "Hospital Alemán",
    "Hospital Rivadavia", "Hospital Pirovano", "Hospital Durand", "Sanatorio Otamendi",
    "Hospital de Clínicas", "Fundación Favaloro", "Hospital Británico", "CEMIC",
    "Sanatorio Mater Dei", "Hospital Santa Isabel", "Clínica del Sol CABA", "Hospital Argerich",
    "Hospital Penna", "Hospital Udaondo", "Hospital Ramos Mejía", "Hospital Tornú",
    "Sanatorio Finochietto", "IADT", "ICBA", "Clínica Suizo Argentina", "Sanatorio Colegiales",
    "Hospital Elizalde", "Hospital Muñiz", "Sanatorio Trinidad", "Clínica La Pequeña Familia"
]

HOSPITALES_GBA_NORTE = [
    "Sanatorio Norte", "Hospital Central San Isidro", "Clínica del Sol Olivos", "Sanatorio San Lucas",
    "Hospital de Tigre", "Clínica Olivos", "Hospital de Vicente López", "Sanatorio Las Lomas",
    "Hospital Austral Pilar", "Clínica San Camilo", "Hospital Zubizarreta Norte", "Sanatorio Modelo Caseros",
    "Hospital de San Fernando", "Clínica San Jorge", "Hospital Municipal de San Martín", "Sanatorio Dr. Julio Méndez"
]

HOSPITALES_GBA_OESTE = [
    "Hospital Posadas", "Hospital Santojanni", "Hospital Cuenca Alta", "Hospital Paroissien",
    "Hospital Narciso López", "Clínica Modelo Morón", "Sanatorio Oeste", "Hospital de Moreno",
    "Hospital de Merlo", "Hospital Evita Pueblo", "Clínica Bazterrica Oeste", "Hospital de La Matanza"
]

HOSPITALES_GBA_SUR = [
    "Hospital Fiorito", "Hospital Gandulfo", "Hospital Arturo Oñativia", "Clínica del Sur",
    "Hospital de Quilmes", "Sanatorio Modelo Quilmes", "Hospital de Lomas de Zamora", "Clínica San Pablo",
    "Hospital de Berazategui", "Hospital de Florencio Varela", "Sanatorio Sur", "Hospital Evita Lanús"
]

ZONAS = ['CABA', 'GBA Norte', 'GBA Oeste', 'GBA Sur']
TIPOS = ['Privado', 'Publico']
POTENCIALES = ['Alto', 'Medio', 'Bajo']
PROBABILIDADES = ['Alta', 'Media-Alta', 'Media', 'Media-Baja', 'Baja']
PRODUCTOS = ['Cofias', 'Paños', 'Incontinencia', 'Descartadores', 'Guantes', 'Protocolo', 'Insumos']
PUESTOS = ['Compras', 'Enfermería', 'Farmacia', 'Director Médico', 'Jefa de Sector', 'Control Infecciones', 'Administración']
INTERESES = ['COFIAS', 'PAÑOS', 'INCONTINENCIA', 'DESCARTADORES', 'PROTOCOLO', 'VARIOS', 'INSUMOS', '']

TITULOS_VISITA = [
    "Control mensual", "Seguimiento pedido", "Entrega muestras", "Reunión comercial",
    "Renovación contrato", "Prospección inicial", "Presentación productos", "Cotización",
    "Capacitación personal", "Resolución reclamo", "Licitación", "Networking",
    "Seguimiento licitación", "Cierre de venta", "Evaluación trimestral", "Visita rutinaria"
]

DETALLES_VISITA = [
    "Reunión productiva, interesados en ampliar pedidos.",
    "Entrega de muestras nuevas. Muy buena recepción.",
    "Control de stock, necesitan reposición.",
    "Seguimiento de cotización enviada la semana pasada.",
    "Capacitación al personal de enfermería sobre nuevos productos.",
    "Primera visita de prospección. Proceso de licitación en curso.",
    "Renovación de contrato anual. Todo OK.",
    "Presentación de nueva línea de incontinencia.",
    "Resolución de reclamo por demora en entrega anterior.",
    "Networking con decisores clave del hospital.",
    "Entrega de pedido urgente. Cliente muy agradecido.",
    "Evaluación de productos en prueba. Feedback positivo.",
    "Reunión con director médico para ampliar línea.",
    "Seguimiento de implementación de protocolo.",
    "Gestión de pagos atrasados."
]

PROXIMOS_PASOS = [
    "Enviar cotización", "Seguimiento en 2 semanas", "Coordinar entrega",
    "Esperar aprobación", "Programar capacitación", "Preparar propuesta",
    "Llamar próxima semana", "Enviar catálogo", "Monitorear licitación",
    "Firmar contrato", "Entregar muestras", "", ""
]

def generar_nombre_contacto():
    nombres = ["María", "Carlos", "Laura", "Diego", "Ana", "Roberto", "Patricia", "Sergio", 
               "Claudia", "Juan", "Silvia", "Martín", "Andrea", "Pablo", "Romina", "Fernando",
               "Gabriela", "Eduardo", "Noelia", "Ricardo", "Daniela", "Alejandro", "Verónica"]
    apellidos = ["González", "Rodríguez", "López", "Martínez", "García", "Fernández", "Pérez",
                 "Sánchez", "Ramírez", "Torres", "Díaz", "Ruiz", "Morales", "Alvarez", "Romero",
                 "Jiménez", "Hernández", "Vargas", "Castro", "Ortiz", "Ríos", "Mendoza"]
    return f"{random.choice(nombres)} {random.choice(apellidos)}"

def generar_telefono():
    return f"11-{random.randint(2000,9999)}-{random.randint(1000,9999)}"

def generar_direccion(zona):
    calles = ["Av. Córdoba", "Av. Santa Fe", "Av. Corrientes", "Av. Las Heras", "Av. del Libertador",
              "Av. Rivadavia", "Av. Juan B. Justo", "Av. Pueyrredón", "Av. Callao", "Av. Entre Ríos"]
    return f"{random.choice(calles)} {random.randint(100, 5000)}, {zona}"

def generar_clientes(vendedor, cantidad, hospitales_pool, zona):
    clientes = []
    hospitales_usados = random.sample(hospitales_pool, min(cantidad, len(hospitales_pool)))
    
    for hospital in hospitales_usados:
        tipo = random.choice(TIPOS)
        es_prospecto = random.random() < 0.15  # 15% prospectos
        estado = "PROSPECTO" if es_prospecto else "CLIENTE"
        panos = 0 if es_prospecto else random.choice([0, 500, 800, 1000, 1500, 2000, 2500, 3000, 4000, 5000])
        potencial = random.choice(POTENCIALES)
        probabilidad = random.choice(PROBABILIDADES)
        direccion = generar_direccion(zona)
        camas = random.choice([100, 150, 200, 250, 300, 400, 500, 600, 800])
        productos = ", ".join(random.sample(PRODUCTOS, random.randint(1, 4)))
        
        clientes.append({
            "data": [hospital, vendedor, estado, panos, zona, tipo, potencial, probabilidad, direccion],
            "meta": {"camas": camas, "productos": productos if not es_prospecto else "", "extra": ""}
        })
    
    return clientes

def generar_contactos(clientes):
    contactos = []
    for cliente in clientes:
        hospital = cliente["data"][0]
        tipo = cliente["data"][5]
        estado = cliente["data"][2]
        
        # 1-3 contactos por hospital
        num_contactos = random.randint(1, 3)
        for _ in range(num_contactos):
            nombre = generar_nombre_contacto()
            puesto = random.choice(PUESTOS)
            telefono = generar_telefono() if random.random() > 0.2 else ""
            interes = random.choice(INTERESES)
            contactos.append([hospital, tipo.upper(), estado, nombre, puesto, telefono, interes])
    
    return contactos

def generar_visitas(clientes, vendedor, fecha_inicio, fecha_fin, visitas_por_dia=4):
    visitas = []
    dias_laborales = []
    
    current = fecha_inicio
    while current <= fecha_fin:
        if current.weekday() < 5:  # Lun-Vie
            dias_laborales.append(current)
        current += timedelta(days=1)
    
    hospitales_cliente = [c["data"][0] for c in clientes if c["data"][2] == "CLIENTE"]
    
    for dia in dias_laborales:
        # 4 visitas por día
        hospitales_del_dia = random.sample(hospitales_cliente, min(visitas_por_dia, len(hospitales_cliente)))
        for hospital in hospitales_del_dia:
            titulo = random.choice(TITULOS_VISITA)
            detalle = random.choice(DETALLES_VISITA)
            proximo = random.choice(PROXIMOS_PASOS)
            fecha_str = dia.strftime("%Y-%m-%d")
            visitas.append([fecha_str, vendedor, hospital.upper(), detalle, proximo, titulo])
    
    return visitas

def main():
    print("🔄 Generando datos realistas...")
    
    todos_clientes = []
    todos_contactos = []
    todas_visitas = []
    meta = {}
    
    # Distribuir hospitales por vendedor y zona
    hospitales_por_vendedor = {
        'Emiliano': (HOSPITALES_CABA[:20] + HOSPITALES_GBA_NORTE[:10], 'CABA'),
        'Agustina': (HOSPITALES_CABA[10:] + HOSPITALES_GBA_OESTE, 'CABA'),
        'Mauricio': (HOSPITALES_GBA_NORTE + HOSPITALES_GBA_SUR, 'GBA Norte')
    }
    
    fecha_inicio = datetime(2025, 7, 1)
    fecha_fin = datetime(2025, 12, 15)
    
    for vendedor in VENDEDORES:
        hospitales_pool, zona_principal = hospitales_por_vendedor[vendedor]
        
        # Generar 30 clientes por vendedor
        clientes = generar_clientes(vendedor, 30, hospitales_pool, zona_principal)
        todos_clientes.extend(clientes)
        
        # Generar contactos
        contactos = generar_contactos(clientes)
        todos_contactos.extend(contactos)
        
        # Generar visitas (4 por día laboral)
        visitas = generar_visitas(clientes, vendedor, fecha_inicio, fecha_fin, visitas_por_dia=4)
        todas_visitas.extend(visitas)
        
        # Agregar meta por hospital
        for cliente in clientes:
            hospital = cliente["data"][0]
            meta[hospital.upper()] = cliente["meta"]
    
    # Construir estructura final
    database = {
        "clientes": [c["data"] for c in todos_clientes],
        "contactos": todos_contactos,
        "visitas": todas_visitas,
        "meta": meta
    }
    
    # Guardar
    with open("data/database.json", "w", encoding="utf-8") as f:
        json.dump(database, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Datos generados:")
    print(f"   • Clientes: {len(database['clientes'])}")
    print(f"   • Contactos: {len(database['contactos'])}")
    print(f"   • Visitas: {len(database['visitas'])}")
    print(f"   • Hospitales con meta: {len(database['meta'])}")
    print(f"\n💾 Guardado en data/database.json")

if __name__ == "__main__":
    main()
