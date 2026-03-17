import urllib.request, re

c = urllib.request.urlopen('https://mireiacast1.github.io/jupyterlite-s3/extensions/jupydrive-s3/static/956.698b70cd333da8a54756.js').read().decode('utf-8')
print('bytes:', len(c))
print('pos 21680-21730:', repr(c[21680:21730]))

# buscar TODOS los patrones que Jekyll podria haber roto
# 1. comillas simples sueltas fuera de strings
# 2. > o < sueltos
# 3. cualquier cosa que no sea JS valido

# buscar donde hay ') ' precedido de algo raro
for m in re.finditer(r'\)', c):
    pos = m.start()
    ctx = c[pos-20:pos+5]
    # si hay algo raro antes del )
    if re.search(r'[^\w\s\'".,{}()\[\]!&|=+\-*/<>:;?@#$%^~`\\]', ctx):
        print(f'pos {pos}: {repr(ctx)}')

# buscar el SVG que queda en el archivo
i = c.find('svgstr')
if i >= 0:
    print('svgstr:', repr(c[i:i+200]))
