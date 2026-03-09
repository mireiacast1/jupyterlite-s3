const fs = require('fs');
const file = 'extensions/jupydrive-s3/static/956.698b70cd333da8a54756.js';
let c = fs.readFileSync(file, 'utf8');

// Fix: change 6 closing braces to 7
c = c.replace(
  'secretAccessKey:""}}}}}}))),',
  'secretAccessKey:""}}}}}}})),'
);

fs.writeFileSync(file, c, 'utf8');
console.log('Fixed. Verify:', c.includes('secretAccessKey:""}}}}}}})),'));
