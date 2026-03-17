import sys
f = 'extensions/jupydrive-s3/static/remoteEntry.20b5a0279ea394f88afa.js'
with open(f, 'rb') as fh:
    c = fh.read()
sys.stdout.write('antes: ' + str(c.count(b'698b70cd333da8a54755')) + '\n')
sys.stdout.flush()
new_c = c.replace(b'698b70cd333da8a54755', b'698b70cd333da8a54756')
with open(f, 'wb') as fh:
    fh.write(new_c)
with open(f, 'rb') as fh:
    verify = fh.read()
sys.stdout.write('56 en disco: ' + str(verify.count(b'698b70cd333da8a54756')) + '\n')
sys.stdout.flush()
