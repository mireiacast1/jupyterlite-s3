(function() {
  const params = new URLSearchParams(window.location.search);

  const accessKeyId = params.get('accessKeyId');
  const secretAccessKey = params.get('secretAccessKey');
  const sessionToken = params.get('sessionToken');
  const bucket = params.get('bucket');
  const region = params.get('region') || 'eu-central-1';
  const root = params.get('root') || '';
  const endpoint = params.get('endpoint') || 'https://c1nl0knyal.execute-api.eu-central-1.amazonaws.com/dev/s3-proxy';

  if (!accessKeyId || !secretAccessKey || !bucket) return;

  const raw = JSON.stringify({
    bucket,
    root,
    endpoint,
    region,
    accessKeyId,
    secretAccessKey
  });

  const settingId = 'jupydrive-s3:auth-file-browser';
  const baseUrl = window.location.pathname.replace(/(\/lab\/?.*|\/index\.html)?$/, '/');
  const storageName = `JupyterLite Storage - ${window.location.origin}${baseUrl}`;

  const req = indexedDB.open(storageName);
  req.onsuccess = function(e) {
    const db = e.target.result;
    if (!db.objectStoreNames.contains('settings')) {
      db.close();
      return;
    }
    const tx = db.transaction('settings', 'readwrite');
    tx.objectStore('settings').put(raw, settingId);
    tx.oncomplete = () => { db.close(); console.log('S3 config saved to IndexedDB'); };
  };
  req.onupgradeneeded = function(e) {
    e.target.result.createObjectStore('settings');
  };
})();
