const fs = require('fs');
const file = 'extensions/jupydrive-s3/static/956.698b70cd333da8a54755.js';
let c = fs.readFileSync(file, 'utf8');

// Patch 1: fix factory() to read window.__s3Params first
c = c.replace(
  '{factory:async()=>{var e,t,i,o,a,r,c;return null!==(e=await(async()=>{const e=s(await n.load(O.id));return""!==e.name?e:null})())&&void 0!==e?e:{name:null!==(t="MISSING_ENV_VAR".JP_S3_BUCKET)&&void 0!==t,root:null!==(i="MISSING_ENV_VAR".JP_S3_ROOT)&&void 0!==i?i:"",config:{forcePathStyle:!0,endpoint:null!==(o="MISSING_ENV_VAR".JP_S3_ENDPOINT)&&void 0!==o?o:"https://example.com/s3",region:null!==(a="MISSING_ENV_VAR".JP_S3_REGION)&&void 0!==a?a:"eu-west-1",credentials:{accessKeyId:null!==(r="MISSING_ENV_VAR".JP_S3_ACCESS_KEY_ID)&&void 0!==r?r:"abcdefghijklmnopqrstuvwxyz",secretAccessKey:null!==(c="MISSING_ENV_VAR".JP_S3_SECRET_ACCESS_KEY)&&void 0!==c?c:"SECRET123456789abcdefghijklmnopqrstuvwxyz"}}}}}}',
  '{factory:async()=>{var e,t,i,o,a,r,c;const _p=window.__s3Params;if(_p&&_p.bucket)return{name:_p.bucket,root:_p.root||"",config:{forcePathStyle:!0,endpoint:_p.endpoint,region:_p.region,credentials:{accessKeyId:_p.accessKeyId,secretAccessKey:_p.secretAccessKey}}};return null!==(e=await(async()=>{const e=s(await n.load(O.id));return""!==e.name?e:null})())&&void 0!==e?e:{name:"",root:"",config:{forcePathStyle:!0,endpoint:"https://example.com/s3",region:"eu-west-1",credentials:{accessKeyId:"",secretAccessKey:""}}}}}'
);

// Patch 2: guard changed.connect to skip when name is empty
c = c.replace(
  'o.changed.connect((()=>{const n=s(o),a=new T({...n,secretsManager:i,token:e});t.serviceManager.contents.addDrive(a)}))',
  'o.changed.connect((()=>{const n=s(o);if(!n.name)return;const a=new T({...n,secretsManager:i,token:e});t.serviceManager.contents.addDrive(a)}))'
);

// Patch 3: guard plugin V activate when name is missing
c = c.replace(
  'activate:async(e,t,n,i,o,s,a,c)=>{const{commands:l}=e,h=await n.factory(),u=new T({name:h.name,root:h.root,config:h.config,secretsManager:h.secretsManager,token:h.token})',
  'activate:async(e,t,n,i,o,s,a,c)=>{const{commands:l}=e,h=await n.factory();if(!h||!h.name)throw new Error("S3 bucket name missing");const u=new T({name:h.name,root:h.root,config:h.config,secretsManager:h.secretsManager,token:h.token})'
);

fs.writeFileSync(file, c, 'utf8');
console.log('Patches applied. Verifying...');

// Count patch applications
const checks = [
  c.includes('window.__s3Params'),
  c.includes('if(!n.name)return'),
  c.includes('S3 bucket name missing')
];
console.log('Patch 1 (factory __s3Params):', checks[0]);
console.log('Patch 2 (guard changed.connect):', checks[1]);
console.log('Patch 3 (guard activate):', checks[2]);
