import shutil, re

# copiar el archivo correcto con un nuevo nombre
src = 'extensions/jupydrive-s3/static/956.698b70cd333da8a54756.js'
dst = 'extensions/jupydrive-s3/static/956.698b70cd333da8a54757.js'
shutil.copy(src, dst)
print(f'copiado a {dst}')

# actualizar remoteEntry para apuntar al nuevo archivo
f = 'extensions/jupydrive-s3/static/remoteEntry.20b5a0279ea394f88afa.js'
with open(f, 'rb') as fh:
    c = fh.read()
new_c = c.replace(b'698b70cd333da8a54756', b'698b70cd333da8a54757')
with open(f, 'wb') as fh:
    fh.write(new_c)
print(f'remoteEntry actualizado: {c.count(b"698b70cd333da8a54756")} -> {new_c.count(b"698b70cd333da8a54757")} refs')
