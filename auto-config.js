window.__s3ConfigReady = new Promise(function(resolve) {
  const params = new URLSearchParams(window.location.search);
  const accessKeyId = params.get('accessKeyId');
  const secretAccessKey = params.get('secretAccessKey');
  const bucket = params.get('bucket');
  const region = params.get('region') || 'eu-central-1';
  const root = params.get('root') || '';
  const endpoint = params.get('endpoint') || 'https://c1nl0knyal.execute-api.eu-central-1.amazonaws.com/dev/s3-proxy';

  if (!accessKeyId || !secretAccessKey || !bucket) { resolve(); return; }

  const raw = JSON.stringify({ bucket, root, endpoint, region, accessKeyId, secretAccessKey });
  const settingId = 'jupydrive-s3:auth-file-browser';
  const baseUrl = window.location.pathname.replace(/(\/lab\/?.*|\/index\.html)?$/, '/');
  const storageName = `JupyterLite Storage - ${window.location.origin}${baseUrl}`;

  function write(db) {
    const tx = db.transaction('settings', 'readwrite');
    tx.objectStore('settings').put(raw, settingId);
    tx.oncomplete = function() { db.close(); console.log('S3 config saved:', { bucket, root, endpoint, region, accessKeyId }); resolve(); };
    tx.onerror = function() { db.close(); resolve(); };
  }

  const req = indexedDB.open(storageName);
  req.onsuccess = function(e) {
    const db = e.target.result;
    if (db.objectStoreNames.contains('settings')) { write(db); }
    else {
      db.close();
      const req2 = indexedDB.open(storageName, db.version + 1);
      req2.onupgradeneeded = function(e) { e.target.result.createObjectStore('settings'); };
      req2.onsuccess = function(e) { write(e.target.result); };
      req2.onerror = function() { resolve(); };
    }
  };
  req.onupgradeneeded = function(e) { e.target.result.createObjectStore('settings'); };
  req.onerror = function() { resolve(); };
});
