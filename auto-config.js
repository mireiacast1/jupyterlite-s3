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
      secretAccessKey: secretAccessKey
    };
    
    // Guardar en formato JupyterLab settings
    const settingsKey = 'jupydrive-s3:auth-file-browser';
    const settings = {
      data: config,
      raw: JSON.stringify(config)
    };
    
    localStorage.setItem(settingsKey, JSON.stringify(settings));
    
    // También guardar en formato alternativo
    localStorage.setItem('jupydrive-s3-config', JSON.stringify(config));
    
    console.log('S3 config saved:', config);
    
    // Limpiar URL (quitar credenciales)
    const cleanUrl = window.location.origin + window.location.pathname;
    window.history.replaceState({}, document.title, cleanUrl);
  }
})();
