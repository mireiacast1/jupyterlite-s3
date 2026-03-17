window.__s3ConfigReady = new Promise(function(resolve) {
  const params = new URLSearchParams(window.location.search);
  const accessKeyId = params.get('accessKeyId');
  const secretAccessKey = params.get('secretAccessKey');
  const bucket = params.get('bucket');
  const region = params.get('region') || 'eu-central-1';
  const root = params.get('root') || '';
  const endpoint = params.get('endpoint') || 'https://c1nl0knyal.execute-api.eu-central-1.amazonaws.com/dev/s3-proxy';

  if (accessKeyId && secretAccessKey && bucket) {
    window.__s3Params = { bucket, root, endpoint, region, accessKeyId, secretAccessKey };
    console.log('S3 config saved:', { bucket, root, endpoint, region, accessKeyId });

    // Inject into JupyterLite's settingsOverrides so ISettingRegistry picks them up
    const configEl = document.getElementById('jupyter-config-data');
    if (configEl) {
      const config = JSON.parse(configEl.textContent || '{}');
      config.settingsOverrides = config.settingsOverrides || {};
      config.settingsOverrides['jupydrive-s3:auth-file-browser'] = {
        bucket, root, endpoint, region, accessKeyId, secretAccessKey
      };
      configEl.textContent = JSON.stringify(config);
    }
  }
  resolve();
});
