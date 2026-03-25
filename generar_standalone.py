#!/usr/bin/env python3
"""
Script para generar sigmaline_standalone.html
Embede el CSS en el HTML y agrega funcionalidad de guardar HTML portable
"""

import re

# Leer archivos
with open('programa.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Agregar CSS extra para el botón destacado
extra_css = '''
/* === BOTÓN GUARDAR HTML DESTACADO === */
.save-html-btn {
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    border: none;
    color: white;
    font-weight: 700;
    padding: 12px 16px;
    border-radius: 12px;
    width: 100%;
    margin-bottom: 15px;
    box-shadow: 0 4px 15px rgba(245, 158, 11, 0.4);
    transition: all 0.3s ease;
    animation: pulseGlow 2s infinite;
}
.save-html-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(245, 158, 11, 0.5);
    background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
}
.save-html-btn i {
    margin-right: 8px;
}
@keyframes pulseGlow {
    0%, 100% { box-shadow: 0 4px 15px rgba(245, 158, 11, 0.4); }
    50% { box-shadow: 0 4px 25px rgba(245, 158, 11, 0.7); }
}

/* Recordatorio toast */
.save-reminder-toast {
    position: fixed;
    top: 20px;
    right: 20px;
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    color: white;
    padding: 16px 24px;
    border-radius: 12px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.2);
    z-index: 9999;
    display: flex;
    align-items: center;
    gap: 12px;
    animation: slideInRight 0.5s ease;
    max-width: 350px;
}
.save-reminder-toast .toast-icon {
    font-size: 1.5rem;
}
.save-reminder-toast .toast-content h6 {
    margin: 0 0 4px 0;
    font-weight: 700;
}
.save-reminder-toast .toast-content p {
    margin: 0;
    font-size: 0.85rem;
    opacity: 0.9;
}
.save-reminder-toast .toast-close {
    background: rgba(255,255,255,0.2);
    border: none;
    color: white;
    padding: 4px 8px;
    border-radius: 6px;
    cursor: pointer;
    margin-left: 8px;
}
@keyframes slideInRight {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}
'''

css = css + extra_css

# 1. Reemplazar link a CSS externo por style embebido
css_link_pattern = r'<link rel="stylesheet" href="styles\.css">'
css_embedded = f'<style>\n{css}\n    </style>'
html = re.sub(css_link_pattern, '', html)

# Insertar CSS después del último link de Google Fonts
html = html.replace(
    '<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700;900&display=swap" rel="stylesheet">',
    '<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700;900&display=swap" rel="stylesheet">\n\n    <!-- CSS Embebido (autocontenido) -->\n    ' + css_embedded
)

# 2. Verificar que el comentario CSS Externo se elimine
html = html.replace('<!-- CSS Externo -->', '')
html = html.replace('<link rel="stylesheet" href="styles.css">', '')

# 3. Agregar botón DESTACADO debajo de Stats (después del nav)
old_nav = '''<div class="nav flex-column gap-2">
                <a onclick="switchView('clients')" id="nav-desk-clients" class="nav-link-desktop active"><i class="bi bi-briefcase-fill"></i> Clientes</a>

                <a onclick="switchView('visits')" id="nav-desk-visits" class="nav-link-desktop"><i class="bi bi-journal-text"></i> Visitas</a>
                <a onclick="switchView('contacts')" id="nav-desk-contacts" class="nav-link-desktop"><i class="bi bi-people-fill"></i> Contactos</a>
                <a onclick="switchView('reports')" id="nav-desk-reports" class="nav-link-desktop"><i class="bi bi-bar-chart-fill"></i> Stats</a>
            </div>'''

new_nav_with_button = '''<div class="nav flex-column gap-2">
                <a onclick="switchView('clients')" id="nav-desk-clients" class="nav-link-desktop active"><i class="bi bi-briefcase-fill"></i> Clientes</a>

                <a onclick="switchView('visits')" id="nav-desk-visits" class="nav-link-desktop"><i class="bi bi-journal-text"></i> Visitas</a>
                <a onclick="switchView('contacts')" id="nav-desk-contacts" class="nav-link-desktop"><i class="bi bi-people-fill"></i> Contactos</a>
                <a onclick="switchView('reports')" id="nav-desk-reports" class="nav-link-desktop"><i class="bi bi-bar-chart-fill"></i> Stats</a>
            </div>
            
            <!-- BOTÓN GUARDAR HTML DESTACADO -->
            <button class="save-html-btn mt-3" onclick="downloadHTMLPortable()">
                <i class="bi bi-download"></i> GUARDAR CAMBIOS
            </button>'''

html = html.replace(old_nav, new_nav_with_button)

# 4. Quitar el botón Guardar HTML de abajo (ya está arriba)
restore_button = '<button class="btn btn-sm btn-outline-light" onclick="triggerRestore()"><i class="bi bi-cloud-upload"></i> Restaurar</button>'
# No agregar duplicado, mantener solo Restaurar

# 5. Agregar función downloadHTMLPortable después de downloadBackup
download_html_function = '''
    function downloadHTMLPortable() {
        try {
            let htmlContent = document.documentElement.outerHTML;
            
            const embeddedData = {
                clients: clientsData,
                visits: visitsData,
                contacts: contactsData,
                meta: hospitalMeta,
                savedAt: new Date().toISOString()
            };
            
            const dataScript = '<scr' + 'ipt id="embeddedData" type="application/json">' + JSON.stringify(embeddedData) + '</scr' + 'ipt>';
            
            if (htmlContent.includes('<script id="embeddedData"')) {
                htmlContent = htmlContent.replace(/<script id="embeddedData"[^>]*>[\\s\\S]*?<\\/script>/, dataScript);
            } else {
                htmlContent = htmlContent.replace('</head>', dataScript + '\\n</head>');
            }
            
            if (!htmlContent.startsWith('<!DOCTYPE')) {
                htmlContent = '<!DOCTYPE html>\\n' + htmlContent;
            }
            
            const blob = new Blob([htmlContent], { type: 'text/html;charset=utf-8' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'sigmaline_' + new Date().toISOString().slice(0,10) + '.html';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            // Marcar como guardado
            localStorage.setItem('sigma_last_saved', new Date().toISOString());
            showAlert('✅ HTML Guardado', 'Archivo descargado. Usá ese archivo la próxima vez para conservar tus datos.', 'success');
        } catch (error) {
            console.error('Error guardando HTML:', error);
            showAlert('Error', 'No se pudo generar el archivo HTML: ' + error.message, 'danger');
        }
    }
    
    // Mostrar recordatorio al iniciar
    function showSaveReminder() {
        // Solo mostrar si hay datos y no se guardó recientemente
        const lastSaved = localStorage.getItem('sigma_last_saved');
        const reminderDismissed = sessionStorage.getItem('save_reminder_dismissed');
        
        if (reminderDismissed) return;
        
        setTimeout(() => {
            const toast = document.createElement('div');
            toast.className = 'save-reminder-toast';
            toast.innerHTML = `
                <div class="toast-icon"><i class="bi bi-exclamation-triangle-fill"></i></div>
                <div class="toast-content">
                    <h6>¡Recordá guardar!</h6>
                    <p>Antes de cerrar, hacé clic en <strong>"GUARDAR CAMBIOS"</strong> para no perder tus datos.</p>
                </div>
                <button class="toast-close" onclick="this.parentElement.remove(); sessionStorage.setItem('save_reminder_dismissed', '1');">✕</button>
            `;
            document.body.appendChild(toast);
            
            // Auto-cerrar después de 10 segundos
            setTimeout(() => {
                if (toast.parentElement) toast.remove();
            }, 10000);
        }, 2000);
    }

'''

# Insertar después de downloadBackup
html = html.replace(
    "showAlert('Backup Creado', 'El archivo de seguridad se ha descargado correctamente.', 'success');\n    }",
    "showAlert('Backup Creado', 'El archivo de seguridad se ha descargado correctamente.', 'success');\n    }" + download_html_function
)

# 6. Agregar función loadEmbeddedData
load_embedded_function = '''
    // === CARGAR DATOS EMBEBIDOS EN EL HTML ===
    function loadEmbeddedData() {
        try {
            const embeddedScript = document.getElementById('embeddedData');
            if (embeddedScript) {
                const data = JSON.parse(embeddedScript.textContent);
                clientsData = data.clients || [];
                visitsData = data.visits || [];
                contactsData = data.contacts || [];
                hospitalMeta = data.meta || {};
                
                contactsData.forEach(c => {
                    if (c[7] === undefined) c[7] = '';
                });
                
                console.log('✅ Datos cargados del HTML embebido:', {
                    clientes: clientsData.length,
                    contactos: contactsData.length,
                    visitas: visitsData.length,
                    guardado: data.savedAt
                });
                return true;
            }
            return false;
        } catch(e) {
            console.warn('⚠️ Error cargando datos embebidos:', e);
            return false;
        }
    }

'''

# Insertar antes de loadDataFromLocal
html = html.replace(
    "// === FALLBACK: Cargar de localStorage ===",
    load_embedded_function + "    // === FALLBACK: Cargar de localStorage ==="
)

# 7. Modificar catch de loadDataFromServer para intentar datos embebidos primero
old_catch = """console.warn('⚠️ No se pudo cargar del servidor, usando datos locales:', e);
            // Fallback a localStorage
            loadDataFromLocal();"""
            
new_catch = """console.warn('⚠️ No se pudo cargar del servidor, intentando datos embebidos...', e);
            // Intentar cargar datos embebidos primero
            if (loadEmbeddedData()) {
                return true;
            }
            // Fallback a localStorage
            loadDataFromLocal();"""

html = html.replace(old_catch, new_catch)

# 8. Llamar showSaveReminder al final de la inicialización
# Buscar donde termina la inicialización
html = html.replace(
    "updateHospitalList();",
    "updateHospitalList();\n        showSaveReminder(); // Mostrar recordatorio de guardado"
)

# Guardar archivo
with open('sigmaline_standalone.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ sigmaline_standalone.html generado correctamente")
print(f"   Tamaño: {len(html):,} bytes")
print("   ✨ Botón GUARDAR CAMBIOS arriba del todo")
print("   ✨ Alerta de recordatorio al iniciar")
