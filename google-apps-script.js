/**
 * SIGMALINE CRM - Google Sheets Sync
 * 
 * INSTRUCCIONES DE INSTALACIÓN:
 * 1. Crear un Google Sheet nuevo llamado "SigmaLine Backup"
 * 2. Crear 3 hojas: "Clientes", "Visitas", "Contactos"
 * 3. Ir a Extensiones → Apps Script
 * 4. Borrar todo el código y pegar este archivo completo
 * 5. Guardar (Ctrl+S)
 * 6. Clic en "Implementar" → "Nueva implementación"
 * 7. Tipo: "Aplicación web"
 * 8. Ejecutar como: "Yo"
 * 9. Quién tiene acceso: "Cualquier persona"
 * 10. Clic en "Implementar" y copiar la URL
 * 11. Pegar la URL en el CRM (programa.html)
 */

// Configuración de columnas para cada hoja
const CONFIG = {
  Clientes: {
    headers: ['Hospital', 'Responsable', 'Estado', 'Paños', 'Zona', 'Tipo', 'Potencial', 'Probabilidad', 'Direccion'],
  },
  Visitas: {
    headers: ['Fecha', 'Vendedor', 'Hospital', 'Detalle', 'Proximo', 'Titulo', 'Productos'],
  },
  Contactos: {
    headers: ['Hospital', 'Tipo', 'Estado', 'Nombre', 'Puesto', 'Telefono', 'Interes', 'Email'],
  }
};

/**
 * Maneja las solicitudes POST desde el CRM
 */
function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    
    // Sincronizar cada tipo de datos
    if (data.clients) syncSheet(ss, 'Clientes', data.clients);
    if (data.visits) syncSheet(ss, 'Visitas', data.visits);
    if (data.contacts) syncSheet(ss, 'Contactos', data.contacts);
    
    // Guardar metadatos si existen
    if (data.meta) {
      const metaSheet = getOrCreateSheet(ss, 'Meta');
      metaSheet.clear();
      metaSheet.getRange(1, 1).setValue(JSON.stringify(data.meta));
    }
    
    // Log de última sincronización
    const logSheet = getOrCreateSheet(ss, 'Log');
    logSheet.appendRow([new Date(), 'Sync OK', data.clients?.length || 0, data.visits?.length || 0, data.contacts?.length || 0]);
    
    return ContentService.createTextOutput(JSON.stringify({
      success: true,
      timestamp: new Date().toISOString(),
      counts: {
        clients: data.clients?.length || 0,
        visits: data.visits?.length || 0,
        contacts: data.contacts?.length || 0
      }
    })).setMimeType(ContentService.MimeType.JSON);
    
  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({
      success: false,
      error: error.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * Maneja las solicitudes GET (para verificar que funciona)
 */
function doGet(e) {
  return ContentService.createTextOutput(JSON.stringify({
    status: 'ok',
    message: 'SigmaLine Sync API is running',
    timestamp: new Date().toISOString()
  })).setMimeType(ContentService.MimeType.JSON);
}

/**
 * Sincroniza una hoja con los datos recibidos
 */
function syncSheet(ss, sheetName, data) {
  const sheet = getOrCreateSheet(ss, sheetName);
  const config = CONFIG[sheetName];
  
  // Limpiar hoja
  sheet.clear();
  
  // Escribir encabezados
  if (config && config.headers) {
    sheet.getRange(1, 1, 1, config.headers.length).setValues([config.headers]);
    sheet.getRange(1, 1, 1, config.headers.length).setFontWeight('bold');
  }
  
  // Escribir datos
  if (data && data.length > 0) {
    // Asegurar que cada fila tenga el número correcto de columnas
    const numCols = config ? config.headers.length : data[0].length;
    const normalizedData = data.map(row => {
      const newRow = [...row];
      while (newRow.length < numCols) newRow.push('');
      return newRow.slice(0, numCols);
    });
    
    sheet.getRange(2, 1, normalizedData.length, numCols).setValues(normalizedData);
  }
}

/**
 * Obtiene o crea una hoja
 */
function getOrCreateSheet(ss, name) {
  let sheet = ss.getSheetByName(name);
  if (!sheet) {
    sheet = ss.insertSheet(name);
  }
  return sheet;
}

/**
 * Función de prueba - ejecutar manualmente para verificar
 */
function testSetup() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  
  // Crear hojas si no existen
  Object.keys(CONFIG).forEach(name => {
    const sheet = getOrCreateSheet(ss, name);
    const config = CONFIG[name];
    sheet.getRange(1, 1, 1, config.headers.length).setValues([config.headers]);
    sheet.getRange(1, 1, 1, config.headers.length).setFontWeight('bold');
  });
  
  // Crear hojas auxiliares
  getOrCreateSheet(ss, 'Meta');
  getOrCreateSheet(ss, 'Log');
  
  Logger.log('✅ Setup completado. Las hojas fueron creadas.');
}
