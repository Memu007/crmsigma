#!/usr/bin/env python3
"""
Script para importar las fichas de hospitales en el CRM.
Agrega/actualiza clientes, contactos y notas de visita.
"""

import json
from datetime import datetime

# Cargar base de datos existente
with open('data/database.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

# Función para encontrar o crear cliente
def find_or_update_client(nombre, responsable="Emiliano", estado="PROSPECTO", panos=0, zona="CABA", tipo="Publico", potencial="Medio", probabilidad="Media", direccion=""):
    for i, c in enumerate(db['clientes']):
        if c[0].upper() == nombre.upper():
            # Actualizar datos existentes si se proporcionan
            if direccion:
                db['clientes'][i][8] = direccion
            return i
    # Crear nuevo cliente
    db['clientes'].append([nombre, responsable, estado, panos, zona, tipo, potencial, probabilidad, direccion])
    return len(db['clientes']) - 1

# Función para agregar contacto si no existe
def add_contact(hospital, nombre, puesto, telefono="", interes="", email=""):
    # Verificar si ya existe
    for c in db['contactos']:
        if c[0].upper() == hospital.upper() and c[3].upper() == nombre.upper():
            return  # Ya existe
    # Agregar nuevo contacto
    # Estructura: [Hospital, Tipo, Estado, Nombre, Puesto, Telefono, Interes, Email]
    db['contactos'].append([hospital, "PRIVADO", "CLIENTE", nombre, puesto, telefono, interes, email])

# Función para agregar visita/nota
def add_visit_note(hospital, detalle, proximo="", titulo="", vendedor="Emiliano", fecha=None):
    if fecha is None:
        fecha = datetime.now().strftime("%Y-%m-%d")
    # Estructura: [Fecha, Vendedor, Hospital, Detalle, Proximo, Titulo, Productos]
    db['visitas'].append([fecha, vendedor, hospital.upper(), detalle, proximo, titulo, ""])

print("=" * 60)
print("IMPORTANDO FICHAS DE HOSPITALES")
print("=" * 60)

# ============================================================
# HOSPITAL TORNÚ
# ============================================================
print("→ Hospital Tornú")
find_or_update_client("Hospital Tornú", "Emiliano", "PROSPECTO", 0, "CABA", "Publico", "Alto", "Alta", "CABA")
add_contact("Hospital Tornú", "Lic. Mariana Turci", "Oficina de Compras", "", "Cofias, Incontinencia", "tornu_compras@buenosaires.gob.ar")
add_contact("Hospital Tornú", "Federico Busello", "Jefe Comité Médico / Capacitación", "", "", "")
add_contact("Hospital Tornú", "Lic. Claudia Lanfranco", "Jefa de Enfermería", "11-68138455", "", "")
add_visit_note("Hospital Tornú", 
    "Presentación/Prueba: Muestras entregadas, evaluadas y APROBADAS. Gestión Comercial: Visita a compras, prueba satisfactoria. Negociación: Intención de cambiar marca anterior (Natural Touch).",
    "Formalización del proceso de compra",
    "Prueba Aprobada - Intención de Cambio de Marca")

# ============================================================
# HOSPITAL ELIZALDE
# ============================================================
print("→ Hospital Elizalde")
find_or_update_client("Hospital Elizalde", "Emiliano", "CLIENTE", 0, "CABA", "Publico", "Alto", "Alta", "CABA")
add_contact("Hospital Elizalde", "Vanessa Roldán", "ECI", "11-56046820", "Paños Pediátricos, Cofias, Incontinencia", "")
add_contact("Hospital Elizalde", "Cinthia", "Jefa Terapia Intensiva", "11-51569197", "", "")
add_visit_note("Hospital Elizalde",
    "Presentación a Jefa Operativa (con Propato). Evaluación técnica en curso. Reunión con jefes de enfermería de UTI, UTM, ECI, Gerencia, Oncología, Traumatología. PRIMER PEDIDO: Paños pediátricos.",
    "Incorporación de cofias e incontinencia en 1-2 meses",
    "Primeros Pedidos Realizados - En Proceso de Incorporación")

# ============================================================
# HOSPITAL MUÑIZ
# ============================================================
print("→ Hospital Muñiz")
find_or_update_client("Hospital Muñiz", "Emiliano", "CLIENTE", 0, "CABA", "Publico", "Alto", "Alta", "CABA")
add_contact("Hospital Muñiz", "Lic. Walter Bertoldi", "Gerente Operativo", "4304-2925", "Incontinencia, Cofias", "muñiz_wbertoldi@buenosaires.gob.ar")
add_contact("Hospital Muñiz", "Lic. Sandra Gagliardo", "Subgte de Enfermería", "11-6801-5364", "", "")
add_contact("Hospital Muñiz", "Lic. Hector Almonacid", "Jefe División Enfermería", "", "", "")
add_visit_note("Hospital Muñiz",
    "Evaluación de productos con equipo. Reunión con Gerente Operativo (contacto Propato). PRIMER PEDIDO: Paños para prueba.",
    "Incorporación de incontinencia y cofias en ~2 meses",
    "Primer Pedido Realizado - En Proceso de Incorporación")

# ============================================================
# HOSPITAL POSADAS
# ============================================================
print("→ Hospital Posadas")
find_or_update_client("Hospital Posadas", "Emiliano", "CLIENTE", 0, "GBA Oeste", "Publico", "Alto", "Alta", "Gran Buenos Aires")
add_contact("Hospital Posadas", "Mariana Calderon", "Coordinadora ECI / Enfermera Neonatóloga", "", "Clorhex Secos, Paños Pediátricos", "")
add_visit_note("Hospital Posadas",
    "CLIENTE EXISTENTE. Usan Paños Classic Clorhex y Jabonosos Secos. Reunión con las 5 ECIS. Les gustaron los Clorhex Secos, gran interés en paños pediátricos.",
    "Expansión de Clorhex Secos y Paños Pediátricos",
    "Cliente Activo - Expansión de Productos")

# ============================================================
# HOSPITAL SAN ISIDRO (Central y Materno Infantil)
# ============================================================
print("→ Hospital San Isidro")
find_or_update_client("Hospital San Isidro", "Emiliano", "PROSPECTO", 0, "San Isidro", "Publico", "Alto", "Media", "San Isidro")
add_contact("Hospital San Isidro", "Lic. Karuchek", "Jefa Enfermería (Htal. Central)", "11-49721064", "Paños Clorhexidina, Pediátricos", "")
add_contact("Hospital San Isidro", "Dra. Tesaire", "Jefa Terapia Infantil (Materno Infantil)", "", "Paños Pediátricos", "")
add_contact("Hospital San Isidro", "Dr. Campi", "Htal. Central", "", "", "")
add_visit_note("Hospital San Isidro",
    "Evaluación Central: Paños gustaron mucho (preoperatorios, turno noche). TRABA: Requiere alta como proveedor en Municipalidad. Materno Infantil: Interés en Clorhexidina y Pediátricos (usan algodón/agua).",
    "Pendiente alta como proveedor municipal",
    "En Prueba - Traba Administrativa")

# ============================================================
# HOSPITAL GUTIÉRREZ
# ============================================================
print("→ Hospital Gutiérrez")
find_or_update_client("Hospital Gutiérrez", "Emiliano", "PROSPECTO", 0, "CABA", "Publico", "Alto", "Alta", "CABA")
add_contact("Hospital Gutiérrez", "Laura", "Coordinadora de Terapia Intensiva", "11-38997484", "Incontinencia, Cofias", "")
add_contact("Hospital Gutiérrez", "Dr. Gatari", "Contacto Inicial", "", "", "")
add_visit_note("Hospital Gutiérrez",
    "Coordinación inicial. Reunión con Coordinadora de Terapia Intensiva.",
    "Entrada de incontinencia/cofias en Terapia a corto plazo. Incorporación a escala en 3 meses",
    "Fase de Presentación - Proyección de Compra")

# ============================================================
# HOSPITAL SAN CAYETANO (Tigre)
# ============================================================
print("→ Hospital San Cayetano")
find_or_update_client("Hospital San Cayetano", "Emiliano", "PROSPECTO", 0, "Tigre", "Publico", "Medio", "Media", "Tigre")
add_contact("Hospital San Cayetano", "Laura Cardoso", "ECI", "11-23087482", "", "")
add_visit_note("Hospital San Cayetano",
    "Primera visita. Interés en incorporar productos (usan paños secos de otra marca). Entrega de paños para evaluación. Capacitaciones coordinadas.",
    "Finalización de prueba de productos",
    "En Evaluación")

# ============================================================
# SANATORIO FINOCHIETTO (ASE / OS Dirección)
# ============================================================
print("→ Sanatorio Finochietto")
find_or_update_client("Sanatorio Finochietto", "Emiliano", "CLIENTE", 0, "CABA", "Privado", "Alto", "Alta", "CABA")
add_contact("Sanatorio Finochietto", "Patricia Estevez", "Jefa de Logística", "3752-8000 int. 8773", "", "pestevez@sanatoriofinochietto.com")
add_contact("Sanatorio Finochietto", "Analia Aguirre", "Compras Médicas", "", "", "aaguirre@ase.com.ar")
add_contact("Sanatorio Finochietto", "Patricio Nanzo", "Coordinador de Logística", "3752-8000 int. 8774", "", "")
add_contact("Sanatorio Finochietto", "Jonathan Damian Husto", "Administración / Pagos", "11-2884-0010", "", "")
add_visit_note("Sanatorio Finochietto",
    "CLIENTE ACTIVO. OC recibida (OC-50639-101) por $218.250. Solicitud urgente por falta stock cepillos. Gestión cobranza facturas vencidas.",
    "Seguimiento cobranza y reposición urgente",
    "Cliente Activo - Flujo de Pedidos")

# ============================================================
# CLÍNICA PASTELEROS
# ============================================================
print("→ Clínica Pasteleros")
find_or_update_client("Clínica Pasteleros", "Emiliano", "CLIENTE", 0, "CABA", "Privado", "Medio", "Alta", "Av. Corrientes 4180, CABA")
add_contact("Clínica Pasteleros", "Johanna Coro", "Dpto. de Compras", "3985-6500 Int. 6547", "Clorhexidina, Manzanilla", "compras1@clinica.pasteleros.org.ar")
add_visit_note("Clínica Pasteleros",
    "CLIENTE ACTIVO. Solicitud presupuesto descartables. OC emitida (PO16933): Paño Clorhexidina y Paño Manzanilla.",
    "Coordinación entrega pedido",
    "Pedidos Recurrentes Confirmados")

# ============================================================
# CEMIC
# ============================================================
print("→ CEMIC")
# Ya existe en DB, actualizar contacto
add_contact("CEMIC", "Maria Gomez", "Pagos/Administración", "", "", "mgomez@cemic.edu.ar")
add_visit_note("CEMIC",
    "CLIENTE ACTIVO. Múltiples gestiones cobranza facturas pendientes desde agosto. Confirmación pago facturas Oct/Nov mediante echeq.",
    "Seguimiento activo de cobranza",
    "Pagos Pendientes en Gestión")

# ============================================================
# SANATORIO ANCHORENA
# ============================================================
print("→ Sanatorio Anchorena")
add_contact("Sanatorio Anchorena", "Pagos Anchorena", "Administración", "", "", "pagos@sanatorio-anchorena.com.ar")
add_visit_note("Sanatorio Anchorena",
    "Reclamo cobranza: +40 días vencidos. Solicitado pago parcial o cronograma. Respuestas genéricas, falta compromiso.",
    "Regularizar pagos",
    "Cobranza con Demoras Significativas")

# ============================================================
# SANATORIO LAS LOMAS (Swiss Medical)
# ============================================================
print("→ Sanatorio Las Lomas (Swiss Medical)")
add_contact("Sanatorio Las Lomas", "Micaela Arzamendia Lagunas", "Compras Descartables", "", "", "micaela.arzamendia@swissmedical.com.ar")
add_contact("Sanatorio Las Lomas", "Santiago Nicolas Romanowicz", "Swiss Medical", "", "", "")
add_contact("Sanatorio Las Lomas", "Yanina Vanesa Marengo", "Swiss Medical", "", "", "")
add_visit_note("Sanatorio Las Lomas",
    "Trámite alta de proveedor. Problema: Facturas no ingresadas correctamente por estructura Swiss Medical. Tramitando regularización.",
    "Alta proveedor y regularización facturación",
    "Trámite Administrativo en Curso")

# ============================================================
# SANATORIO FRANCHIN
# ============================================================
print("→ Sanatorio Franchin")
find_or_update_client("Sanatorio Franchin", "Emiliano", "PROSPECTO", 0, "CABA", "Privado", "Medio", "Media", "CABA")
add_contact("Sanatorio Franchin", "Reyna del Vicci", "ECI", "11-67125700", "", "")
add_visit_note("Sanatorio Franchin",
    "Presentación de productos. Muestras entregadas para evaluación. Seguimiento activo en compras.",
    "Esperar resultado evaluación",
    "Muestras en Prueba")

# ============================================================
# CLÍNICA BAZTERRICA
# ============================================================
print("→ Clínica Bazterrica")
add_contact("Clínica Bazterrica", "Lic. Panihuara", "Jefa Enf/ECI", "11-39386963", "", "")
add_contact("Clínica Bazterrica", "Luna Romero", "Farmacia", "", "", "")
add_visit_note("Clínica Bazterrica",
    "Prueba de productos conseguida, en curso de evaluación.",
    "Esperar resultado evaluación",
    "Muestras en Prueba")

# ============================================================
# HOSPITAL ROFFO
# ============================================================
print("→ Hospital Roffo")
find_or_update_client("Hospital Roffo", "Emiliano", "PROSPECTO", 0, "CABA", "Publico", "Medio", "Media", "CABA")
add_contact("Hospital Roffo", "Elba Gonzales", "Jefa Operativa", "11-37679823", "", "")
add_contact("Hospital Roffo", "Sabrina Ideal", "ECI", "11-66902439", "", "")
add_visit_note("Hospital Roffo",
    "Primera visita. Paños dejados para evaluación.",
    "Esperar resultado prueba",
    "Muestras en Prueba")

# ============================================================
# HOSPITAL BRITÁNICO
# ============================================================
print("→ Hospital Británico")
add_contact("Hospital Británico", "Gustavo", "Gestión Reingreso", "", "", "")
add_visit_note("Hospital Británico",
    "Seguimiento para reingreso de productos. Gustavo realizando gestiones administrativas.",
    "Completar gestión reingreso",
    "Reingreso en Gestión")

# ============================================================
# HOSPITAL PEDIÁTRICO TIGRE
# ============================================================
print("→ Hospital Pediátrico Tigre")
find_or_update_client("Hospital Pediátrico Tigre", "Emiliano", "PROSPECTO", 0, "Tigre", "Publico", "Medio", "Alta", "Tigre")
add_contact("Hospital Pediátrico Tigre", "Lic. Ambrosio", "Jefa Farmacia", "", "", "")
add_visit_note("Hospital Pediátrico Tigre",
    "Evaluación positiva informada por Jefa de Farmacia. Confirmada intención de incorporar productos este mes.",
    "Cerrar incorporación",
    "Próxima Incorporación - Evaluación Positiva")

# ============================================================
# HOSPITAL RIVADAVIA
# ============================================================
print("→ Hospital Rivadavia")
add_contact("Hospital Rivadavia", "Supervisora de Enfermería", "Supervisora", "", "Paños Pediátricos", "")
add_contact("Hospital Rivadavia", "Jefe de Enfermería (Cesis)", "Jefe de Enfermería", "", "Paños Pediátricos", "")
add_visit_note("Hospital Rivadavia",
    "Interés específico en paños pediátricos durante presentación.",
    "Seguir con foco en paños pediátricos",
    "En Presentación - Foco Producto Específico")

# ============================================================
# HOSPITAL FERRER
# ============================================================
print("→ Hospital Ferrer")
find_or_update_client("Hospital Ferrer", "Emiliano", "PROSPECTO", 0, "CABA", "Publico", "Medio", "Media", "CABA")
add_contact("Hospital Ferrer", "Lic. Marco Fidalgo", "Gerente Operativo", "", "", "")
add_contact("Hospital Ferrer", "Farmac. Laura Benzal", "Farmacia", "", "", "")
add_visit_note("Hospital Ferrer",
    "Contacto de presentación inicial. Coordinar reunión con Enfermería y entrega de muestras en Farmacia.",
    "Coordinar reunión con Enfermería",
    "Primer Contacto - Coordinando Reunión")

# ============================================================
# HOSPITAL ZUBIZARRETA
# ============================================================
print("→ Hospital Zubizarreta")
find_or_update_client("Hospital Zubizarreta", "Emiliano", "CLIENTE", 0, "CABA", "Publico", "Medio", "Media", "CABA")
add_contact("Hospital Zubizarreta", "Liliana", "Contacto Capacitaciones", "", "", "")
add_visit_note("Hospital Zubizarreta",
    "Historial de capacitaciones realizadas. Contacto para coordinar nuevas capacitaciones.",
    "Coordinar nuevas capacitaciones",
    "Relacionamiento - Foco en Capacitación")

# ============================================================
# HOSPITAL BICENTENARIO (Tucumán)
# ============================================================
print("→ Hospital Bicentenario (Tucumán)")
find_or_update_client("Hospital Bicentenario", "Emiliano", "PROSPECTO", 0, "Tucumán", "Publico", "Medio", "Media", "Tucumán")
add_contact("Hospital Bicentenario", "Rosa Mayan", "Jefa de Enfermería y Depósito", "11-66638942", "", "")
add_visit_note("Hospital Bicentenario",
    "Visita con Propato. Muy buena recepción. Muestras dejadas para prueba del equipo de enfermería y control de infecciones.",
    "Esperar resultado evaluación",
    "En Evaluación - Buena Recepción")

# ============================================================
# GUARDAR BASE DE DATOS
# ============================================================
print("=" * 60)
print("Guardando base de datos...")

with open('data/database.json', 'w', encoding='utf-8') as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

print(f"✅ Importación completada!")
print(f"   - Clientes: {len(db['clientes'])}")
print(f"   - Contactos: {len(db['contactos'])}")
print(f"   - Visitas: {len(db['visitas'])}")
print("=" * 60)
print("\n🚀 Ahora podés iniciar el servidor con: python3 server.py")
