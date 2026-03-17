import re, base64, subprocess

for filename in [
    'extensions/jupydrive-s3/static/956.698b70cd333da8a54755.js',
    'extensions/jupydrive-s3/static/956.698b70cd333da8a54756.js',
]:
    result = subprocess.run(['git', 'show', 'HEAD~3:' + filename], capture_output=True)
    c = result.stdout.decode('utf-8')

    def encode_svg(m):
        full = m.group(0)  # svgstr:'...'
        inner = full[8:-1]  # contenido crudo con escapes JS
        # eliminar el comentario JS-escaped: \x3c!-- ... --\x3e
        inner = re.sub(r'\\x3c!--.*?--\\x3e', '', inner, flags=re.DOTALL)
        # encodear el inner tal cual (con sus escapes JS) en base64
        b64 = base64.b64encode(inner.encode('utf-8')).decode('ascii')
        return "svgstr:'data:image/svg+xml;base64," + b64 + "'"

    new_c = re.sub(r"svgstr:'.*?'(?=[,}])", encode_svg, c, flags=re.DOTALL)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(new_c)
    print(f'{filename}: ok, bytes={len(new_c)}')
    
    # verificar que no hay <!-- en el base64 decodificado
    for m in re.finditer(r"svgstr:'data:image/svg\+xml;base64,([^']+)'", new_c):
        decoded = base64.b64decode(m.group(1)).decode('utf-8')
        print(f'  comentarios HTML: {decoded.count("<!--")}')
        print(f'  comillas dobles: {decoded.count(chr(34))}')
