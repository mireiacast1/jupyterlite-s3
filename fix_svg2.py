import re

for filename in [
    'extensions/jupydrive-s3/static/956.698b70cd333da8a54755.js',
    'extensions/jupydrive-s3/static/956.698b70cd333da8a54756.js',
]:
    with open(filename, 'r', encoding='utf-8') as f:
        c = f.read()

    # Revertir: cambiar comillas simples de vuelta a \" (escapadas para JS)
    # dentro de los SVGs: xmlns='...' -> xmlns=\"...\"
    def fix_svg(m):
        svg = m.group(0)
        # solo reemplazar comillas simples que son atributos XML (precedidas por =)
        return re.sub(r"='([^']*)'", lambda a: '=\\"' + a.group(1) + '\\"', svg)

    new_c = re.sub(r"svgstr:'.*?'(?=[,}])", fix_svg, c, flags=re.DOTALL)

    changed = c != new_c
    print(f'{filename}: changed={changed}')

    if changed:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_c)
        # verificar que el JS sigue siendo valido (no hay comillas simples sueltas en atributos)
        svgs = re.findall(r"svgstr:'.*?'(?=[,}])", new_c, flags=re.DOTALL)
        for svg in svgs:
            print(f'  preview: {repr(svg[:120])}')
