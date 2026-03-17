import re

for filename in [
    'extensions/jupydrive-s3/static/956.698b70cd333da8a54755.js',
    'extensions/jupydrive-s3/static/956.698b70cd333da8a54756.js',
]:
    with open(filename, 'r', encoding='utf-8') as f:
        c = f.read()

    # El delimitador real es una comilla simple ' (no escapada)
    # svgstr:'<svg ...>'  donde las comillas dobles son literales dentro del SVG
    def fix_svg(m):
        return m.group(0).replace('"', "'")

    # patron: svgstr: seguido de ' ... ' (comilla simple como delimitador)
    new_c = re.sub(r"svgstr:'.*?'(?=[,}])", fix_svg, c, flags=re.DOTALL)
    
    changed = c != new_c
    print(f'{filename}: changed={changed}')
    
    if changed:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_c)
        # verificar
        svgs = re.findall(r"svgstr:'.*?'(?=[,}])", new_c, flags=re.DOTALL)
        for svg in svgs:
            print(f'  comillas dobles restantes: {svg.count(chr(34))}')
            print(f'  preview: {repr(svg[:80])}')
