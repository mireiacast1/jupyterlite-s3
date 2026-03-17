import re, base64

c = open('extensions/jupydrive-s3/static/956.698b70cd333da8a54756.js', encoding='utf-8').read()

matches = list(re.finditer(r"svgstr:'data:image/svg\+xml;base64,([^']+)'", c))
print('svgstr encontrados:', len(matches))
for m in matches:
    decoded = base64.b64decode(m.group(1)).decode('utf-8')
    print('SVG tail:', repr(decoded[-300:]))
