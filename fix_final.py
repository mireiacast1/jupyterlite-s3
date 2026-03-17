import re, subprocess

for filename in [
    'extensions/jupydrive-s3/static/956.698b70cd333da8a54755.js',
    'extensions/jupydrive-s3/static/956.698b70cd333da8a54756.js',
    'extensions/jupydrive-s3/static/956.698b70cd333da8a54757.js',
]:
    result = subprocess.run(['git', 'show', 'ffd1fec:' + filename.replace('54757','54756').replace('54755','54756')], capture_output=True)
    if result.returncode != 0:
        result = subprocess.run(['git', 'show', 'ffd1fec:' + filename], capture_output=True)
    c = result.stdout.decode('utf-8')

    # eliminar el comentario HTML escapado
    c = re.sub(r'\\x3c!--.*?--\\x3e', '', c, flags=re.DOTALL)

    # eliminar saltos de linea reales dentro de svgstr (Jekyll los inserta)
    # los svgstr usan \n escapado como \\n, no saltos reales
    # si hay saltos reales dentro de la string, los eliminamos
    def fix_newlines(m):
        return m.group(0).replace('\n', '').replace('\r', '')
    
    c = re.sub(r"svgstr:'.*?'(?=[,}])", fix_newlines, c, flags=re.DOTALL)

    with open(filename, 'w', encoding='utf-8', newline='') as f:
        f.write(c)
    
    # verificar con node
    import subprocess as sp
    r = sp.run(['node', '--check', filename], capture_output=True, text=True)
    print(f'{filename}: node check = {"OK" if r.returncode == 0 else r.stderr[:100]}')
