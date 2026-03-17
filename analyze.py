import urllib.request, re

c = urllib.request.urlopen('https://mireiacast1.github.io/jupyterlite-s3/extensions/jupydrive-s3/static/956.698b70cd333da8a54756.js').read().decode('utf-8')
print('bytes:', len(c))

# buscar entidades HTML
entities = re.findall(r'&[a-zA-Z#0-9]+;', c)
print('entidades HTML:', entities[:10])

# buscar caracteres no ASCII
for i, ch in enumerate(c):
    if ord(ch) > 127:
        print(f'char no-ASCII pos {i}: {repr(ch)} ord={ord(ch)}')
        if i > 100:
            break

# buscar el ')' que falla buscando patrones rotos alrededor de posicion 22073
# pero el archivo tiene 27783 bytes ahora, la posicion puede haber cambiado
# buscar cualquier ')' precedido de algo raro
matches = list(re.finditer(r'[^a-zA-Z0-9_\s\'".,{}()\[\]!&|=+\-*/<>:;?@#$%^~`\\]', c))
print('chars raros:', [(m.start(), repr(m.group())) for m in matches[:10]])
