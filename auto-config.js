(function() {
  const params = new URLSearchParams(window.location.search);
  
  const accessKeyId = params.get('accessKeyId');
  const secretAccessKey = params.get('secretAccessKey');
  const sessionToken = params.get('sessionToken');
  const bucket = params.get('bucket');
  const region = params.get('region') || 'eu-central-1';
  const root = params.get('root') || '';
  const endpoint = params.get('endpoint') || `https://c1nl0knyal.execute-api.eu-central-1.amazonaws.com/dev/s3-proxy/${bucket}`;
  
  if (accessKeyId && secretAccessKey && bucket) {
    const config = {
      bucket: bucket,
      root: root,
      endpoint: `https://c1nl0knyal.execute-api.eu-central-1.amazonaws.com/dev/s3-proxy`,
      region: region,
      accessKeyId: accessKeyId,
      secretAccessKey: secretAccessKey,
      sessionToken: sessionToken || ''
    };
    
    const settingsKey = 'jupyterlab-settings:jupydrive-s3:auth-file-browser';
    localStorage.setItem(settingsKey, JSON.stringify({
      id: 'jupydrive-s3:auth-file-browser',
      data: config,
      raw: JSON.stringify(config),
      schema: {},
      version: ''
    }));
    
    console.log('S3 config saved:', config);
  }
})();
