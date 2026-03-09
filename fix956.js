const fs = require('fs');

// Rename the JS file with a new hash
const oldFile = 'extensions/jupydrive-s3/static/956.698b70cd333da8a54755.js';
const newHash = '698b70cd333da8a54756'; // increment last digit
const newFile = `extensions/jupydrive-s3/static/956.${newHash}.js`;
fs.copyFileSync(oldFile, newFile);

// Update remoteEntry to point to new hash
const remoteFile = 'extensions/jupydrive-s3/static/remoteEntry.20b5a0279ea394f88afa.js';
let r = fs.readFileSync(remoteFile, 'utf8');
r = r.replace(/956:"698b70cd333da8a54755"/g, `956:"${newHash}"`);
r = r.replace(/698b70cd333da8a54755/g, newHash);
fs.writeFileSync(remoteFile, r, 'utf8');

console.log('Done. New file:', newFile);
console.log('remoteEntry updated:', r.includes(newHash));
