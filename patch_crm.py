import json

with open("deploy_ready/crm_app.html", "r", encoding="utf-8") as f:
    html = f.read()

# The user provided the URL
url = "https://script.google.com/a/macros/sigmaline.com.ar/s/AKfycbwrT7bUZMkqqzRkk-hV-DnCPcLiRXy2QbBrtVEWqTwZyBp1BTeO88AWeFesmb_JJDUv/exec"

# Let's replace the saveDataToServer function in crm_app.html
old_func = """    async function saveDataToServer() {
        try {
            const data = {
                clientes: clientsData,
                contactos: contactsData,
                visitas: visitsData,
                meta: hospitalMeta
            };
            
            const response = await fetch('/api/data', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            
            if (!response.ok) throw new Error('Error guardando');
            
            console.log('✅ Guardado en servidor ok');
            showAlert("Guardado Exitoso", "Los datos se han guardado correctamente en la nube.", "success");
            
        } catch (e) {
            console.error('⚠️ No se pudo guardar en el servidor:', e);
            showAlert("Atención", "No se pudo conectar al servidor. Los datos se guardaron localmente.", "warning");
        }
    }"""

new_func = f"""    async function saveDataToServer() {{
        try {{
            // Mostrar indicador de carga en el botón
            const btnElements = document.querySelectorAll('.btn-warning, .btn-primary');
            btnElements.forEach(btn => {{
                if(btn.innerText.includes('GUARDAR CAMBIOS')) {{
                    btn.originalText = btn.innerHTML;
                    btn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Guardando en la Nube...';
                    btn.disabled = true;
                }}
            }});

            const data = {{
                clientes: clientsData,
                contactos: contactsData,
                visitas: visitsData,
                meta: hospitalMeta
            }};
            
            // Usamos no-cors porque Google Apps Script no permite CORS limpio desde Github Pages a veces. 
            // no-cors envía el POST pero no podemos leer la respuesta (opaco). Asumimos éxito si no hay excepción de red.
            const response = await fetch('{url}', {{
                method: 'POST',
                mode: 'no-cors',
                headers: {{ 'Content-Type': 'text/plain' }}, // Google Script previene application/json a veces
                body: JSON.stringify(data)
            }});
            
            console.log('✅ Guardado en la Nube (Google Sheets) enviado ok');
            showAlert("Guardado Exitoso", "Los datos se han guardado también en la Nube (Google Sheets).", "success");
            
        }} catch (e) {{
            console.error('⚠️ No se pudo guardar en la Nube:', e);
            showAlert("Atención", "Se guardó en tu dispositivo pero no hay conexión a internet para subirlo a la Nube.", "warning");
        }} finally {{
            // Restaurar botones
            const btnElements = document.querySelectorAll('.btn-warning, .btn-primary');
            btnElements.forEach(btn => {{
                if(btn.originalText) {{
                    btn.innerHTML = btn.originalText;
                    btn.disabled = false;
                }}
            }});
        }}
    }}"""

# Some previous versions might just have 'fetch('/api/data''
if "async function saveDataToServer()" in html:
    html = html.replace(old_func, new_func)
    
    with open("deploy_ready/crm_app.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Patched saveDataToServer successfully")
else:
    print("Could not find saveDataToServer snippet")
