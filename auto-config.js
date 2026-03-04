(function() {
  const params = new URLSearchParams(window.location.search);
  
  const accessKeyId = params.get('accessKeyId');
  const secretAccessKey = params.get('secretAccessKey');
  const sessionToken = params.get('sessionToken');
  const bucket = params.get('bucket');
  const region = params.get('region') || 'eu-central-1';
  const root = params.get('root') || '';
  
  if (accessKeyId && secretAccessKey && bucket) {
    const config = {
      bucket: bucket,
      root: root,
      endpoint: `https://s3.${region}.amazonaws.com`,
      region: region,
      accessKeyId: accessKeyId,
      secretAccessKey: secretAccessKey,
      sessionToken: sessionToken || ''
    };
    
    // Guardar directamente en el formato que JupyterLab espera
    const settingsKey = 'jupyterlab-settings:jupydrive-s3:auth-file-browser';
    localStorage.setItem(settingsKey, JSON.stringify({
      id: 'jupydrive-s3:auth-file-browser',
      data: config,
      raw: JSON.stringify(config),
      schema: {},
      version: ''
    }));
    
    console.log('S3 config saved:', config);
    
    // Limpiar URL y recargar
    const cleanUrl = window.location.origin + window.location.pathname;
    window.history.replaceState({}, document.title, cleanUrl);
  }
})();
