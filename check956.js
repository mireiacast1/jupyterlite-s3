const c = require('fs').readFileSync('extensions/jupydrive-s3/static/956.698b70cd333da8a54755.js','utf8');
console.log('__s3Params:', c.includes('window.__s3Params'));
console.log('guard connect:', c.includes('if(!n.name)return'));
console.log('guard activate:', c.includes('S3 bucket name missing'));
console.log('broken MISSING_ENV_VAR still present:', c.includes('&&void 0!==t,root:'));
