/**
 * Auto-load notebook from URL parameter
 * Supports: ?fromURL=ENCODED_URL
 */
(async function() {
    console.log('🔧 Notebook Loader initialized');
    
    // Obtener parámetro fromURL
    const params = new URLSearchParams(window.location.search);
    const notebookUrl = params.get('fromURL');
    
    if (!notebookUrl) {
        console.log('ℹ️ No fromURL parameter found');
        return;
    }
    
    console.log('📥 Loading notebook from:', notebookUrl);
    
    try {
        // Esperar a que JupyterLab esté listo
        await waitForJupyterLab();
        
        console.log('✅ JupyterLab ready');
        
        // Descargar notebook
        const response = await fetch(notebookUrl);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const notebookContent = await response.json();
        console.log('✅ Notebook downloaded');
        
        // Obtener nombre del archivo
        const urlObj = new URL(notebookUrl);
        const s3uri = urlObj.searchParams.get('s3uri');
        const notebookName = s3uri ? s3uri.split('/').pop() : 'notebook.ipynb';
        
        console.log('📓 Notebook name:', notebookName);
        
        // Guardar en filesystem de JupyterLite
        const { contents } = window.jupyterapp;
        
        // Crear/sobrescribir archivo
        await contents.save(notebookName, {
            type: 'notebook',
            format: 'json',
            content: notebookContent
        });
        
        console.log('💾 Notebook saved to filesystem');
        
        // Abrir notebook
        await window.jupyterapp.commands.execute('docmanager:open', {
            path: notebookName
        });
        
        console.log('✅ Notebook opened');
        
    } catch (error) {
        console.error('❌ Error loading notebook:', error);
        
        // Mostrar error al usuario
        showError(`Failed to load notebook: ${error.message}`);
    }
})();

/**
 * Espera a que JupyterLab esté completamente cargado
 */
function waitForJupyterLab() {
    return new Promise((resolve) => {
        const checkInterval = setInterval(() => {
            if (window.jupyterapp && window.jupyterapp.commands) {
                clearInterval(checkInterval);
                // Esperar un poco más para asegurar que todo esté listo
                setTimeout(resolve, 1000);
            }
        }, 100);
    });
}

/**
 * Muestra error en la UI
 */
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #f8d7da;
        color: #721c24;
        padding: 15px 20px;
        border-radius: 8px;
        border: 1px solid #f5c6cb;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 10000;
        max-width: 400px;
        font-family: Arial, sans-serif;
    `;
    errorDiv.innerHTML = `
        <strong>⚠️ Error</strong><br>
        ${message}
    `;
    document.body.appendChild(errorDiv);
    
    // Auto-remove después de 10 segundos
    setTimeout(() => errorDiv.remove(), 10000);
}
