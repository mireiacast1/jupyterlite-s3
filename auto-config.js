(function() {
  const params = new URLSearchParams(window.location.search);
  
  const accessKeyId = params.get('accessKeyId');
  const secretAccessKey = params.get('secretAccessKey');
  const sessionToken = params.get('sessionToken');
  const bucket = params.get('bucket');
  const region = params.get('region');
  const root = params.get('root');
  
  if (accessKeyId && secretAccessKey && bucket) {
    const config = {
      bucket: bucket,
      root: root || '',
      endpoint: `https://s3.${region || 'eu-central-1'}.amazonaws.com`,
      region: region || 'eu-central-1',
      accessKeyId: accessKeyId,
      secretAccessKey: secretAccessKey
    };
    
    // Guardar en localStorage para jupydrive-s3
    localStorage.setItem('jupydrive-s3:auth-file-browser', JSON.stringify(config));
    
    // Limpiar URL (quitar credenciales)
    const cleanUrl = window.location.origin + window.location.pathname;
    window.history.replaceState({}, document.title, cleanUrl);
  }
})();
