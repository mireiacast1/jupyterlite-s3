import re, base64

for filename in [
    'extensions/jupydrive-s3/static/956.698b70cd333da8a54755.js',
    'extensions/jupydrive-s3/static/956.698b70cd333da8a54756.js',
]:
    with open(filename, 'r', encoding='utf-8') as f:
        c = f.read()

    def encode_svg(m):
        full = m.group(0)  # svgstr:'<svg...>'
        # extraer el SVG (entre las comillas simples)
        svg = full[8:-1]  # quitar svgstr:' y '
        # encodear en base64 como data URI
        b64 = base64.b64encode(svg.encode('utf-8')).decode('ascii')
        return "svgstr:'data:image/svg+xml;base64," + b64 + "'"

    new_c = re.sub(r"svgstr:'.*?'(?=[,}])", encode_svg, c, flags=re.DOTALL)

    changed = c != new_c
    print(f'{filename}: changed={changed}')

    if changed:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_c)
        print(f'  ok - SVGs reemplazados por data URIs base64')
