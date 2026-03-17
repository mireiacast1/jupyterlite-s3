(function () {
  const params = new URLSearchParams(window.location.search);
  const accessKeyId = params.get('accessKeyId');
  const secretAccessKey = params.get('secretAccessKey');
  const bucket = params.get('bucket');
  const region = params.get('region') || 'eu-central-1';
  const root = params.get('root') || '';
  const endpoint = params.get('endpoint') || 'https://c1nl0knyal.execute-api.eu-central-1.amazonaws.com/dev/s3-proxy';

  if (!(accessKeyId && secretAccessKey && bucket)) {
    window.__s3ConfigReady = Promise.resolve();
    return;
  }

  window.__s3Params = { bucket, root, endpoint, region, accessKeyId, secretAccessKey };
  console.log('S3 config saved:', { bucket, root, endpoint, region, accessKeyId });

  const sessionToken = params.get('sessionToken') || '';
  window.__s3Params = { bucket, root, endpoint, region, accessKeyId, secretAccessKey, sessionToken };
  const s3Settings = { bucket, root, endpoint, region, accessKeyId, secretAccessKey };

  // Intercept fetch so config-utils.js gets settingsOverrides injected into jupyter-lite.json
  const _fetch = window.fetch.bind(window);
  window.fetch = async function (input, init) {
    const url = typeof input === 'string' ? input : input instanceof Request ? input.url : String(input);
    const response = await _fetch(input, init);

    if (/jupyter-lite\.json(\?|$)/.test(url)) {
      const json = await response.json();
      const configData = json['jupyter-config-data'] || {};
      configData['settingsOverrides'] = Object.assign(
        configData['settingsOverrides'] || {},
        { 'jupydrive-s3:auth-file-browser': s3Settings }
      );
      json['jupyter-config-data'] = configData;
      return new Response(JSON.stringify(json), {
        status: response.status,
        headers: response.headers
      });
    }

    return response;
  };

  window.__s3ConfigReady = Promise.resolve();
})();
