/**
 * SigmaLine CRM - Módulo de Google Sheets
 * Conecta el CRM con Google Sheets como backend
 */

const GOOGLE_SHEETS_CONFIG = {
    SHEET_ID: '1HO4YadtnLhIyY4aB4SP4IWCXuH1EIAj0Io6nNfS0kiA',
    API_KEY: 'AIzaSyDmiDWCSrREJzCUCU8Z5eguvVE_NI4-PT0',
    SHEETS: {
        CLIENTES: 'Clientes',
        VISITAS: 'Visitas',
        CONTACTOS: 'Contactos',
        META: 'Meta'
    }
};

/**
 * Leer datos de una pestaña de Google Sheets
 * @param {string} sheetName - Nombre de la pestaña (Clientes, Visitas, etc)
 * @returns {Promise<Array>} - Array de arrays con los datos
 */
async function readFromGoogleSheet(sheetName) {
    const url = `https://sheets.googleapis.com/v4/spreadsheets/${GOOGLE_SHEETS_CONFIG.SHEET_ID}/values/${sheetName}?key=${GOOGLE_SHEETS_CONFIG.API_KEY}`;
    
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Error ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        const rows = data.values || [];
        
        // Si hay encabezados, los removemos (primera fila)
        if (rows.length > 0) {
            return rows.slice(1); // Retorna sin la fila de encabezados
        }
        return [];
    } catch (error) {
        console.error(`Error leyendo ${sheetName} de Google Sheets:`, error);
        throw error;
    }
}

/**
 * Escribir datos a una pestaña de Google Sheets
 * Nota: Para escribir se necesita OAuth2, no solo API Key
 * Por ahora usamos un proxy o Apps Script para escribir
 * @param {string} sheetName - Nombre de la pestaña
 * @param {Array} data - Datos a escribir
 */
async function writeToGoogleSheet(sheetName, data) {
    // Para escritura necesitamos usar un endpoint diferente
    // Opción 1: Google Apps Script como proxy (recomendado)
    // Opción 2: OAuth2 completo (más complejo)
    
    // Por ahora, guardamos localmente y sincronizamos manualmente
    console.warn('Escritura a Google Sheets requiere Apps Script. Guardando localmente.');
    
    // Guardar en servidor local como backup
    try {
        await fetch('/api/data', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ [sheetName.toLowerCase()]: data })
        });
    } catch (e) {
        console.error('Error guardando backup local:', e);
    }
}

/**
 * Cargar todos los datos desde Google Sheets
 * @returns {Promise<Object>} - Objeto con clientes, visitas, contactos, meta
 */
async function loadAllFromGoogleSheets() {
    try {
        const [clientes, visitas, contactos, meta] = await Promise.all([
            readFromGoogleSheet(GOOGLE_SHEETS_CONFIG.SHEETS.CLIENTES),
            readFromGoogleSheet(GOOGLE_SHEETS_CONFIG.SHEETS.VISITAS),
            readFromGoogleSheet(GOOGLE_SHEETS_CONFIG.SHEETS.CONTACTOS),
            readFromGoogleSheet(GOOGLE_SHEETS_CONFIG.SHEETS.META)
        ]);
        
        // Convertir meta de array a objeto
        const metaObj = {};
        meta.forEach(row => {
            if (row[0]) {
                metaObj[row[0].toUpperCase()] = {
                    camas: parseInt(row[1]) || 0,
                    productos: row[2] || '',
                    extra: row[3] || ''
                };
            }
        });
        
        console.log('✅ Datos cargados de Google Sheets:', {
            clientes: clientes.length,
            visitas: visitas.length,
            contactos: contactos.length,
            meta: Object.keys(metaObj).length
        });
        
        return {
            clientes,
            visitas,
            contactos,
            meta: metaObj
        };
    } catch (error) {
        console.error('Error cargando datos de Google Sheets:', error);
        throw error;
    }
}

/**
 * Verificar conexión con Google Sheets
 * @returns {Promise<boolean>}
 */
async function testGoogleSheetsConnection() {
    try {
        const url = `https://sheets.googleapis.com/v4/spreadsheets/${GOOGLE_SHEETS_CONFIG.SHEET_ID}?key=${GOOGLE_SHEETS_CONFIG.API_KEY}`;
        const response = await fetch(url);
        
        if (response.ok) {
            const data = await response.json();
            console.log('✅ Conexión exitosa a:', data.properties.title);
            return true;
        }
        return false;
    } catch (error) {
        console.error('❌ Error de conexión:', error);
        return false;
    }
}

// Exportar funciones para uso global
window.GoogleSheets = {
    read: readFromGoogleSheet,
    write: writeToGoogleSheet,
    loadAll: loadAllFromGoogleSheets,
    testConnection: testGoogleSheetsConnection,
    config: GOOGLE_SHEETS_CONFIG
};
