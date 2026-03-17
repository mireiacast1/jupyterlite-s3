import re, subprocess

for filename in [
    'extensions/jupydrive-s3/static/956.698b70cd333da8a54755.js',
    'extensions/jupydrive-s3/static/956.698b70cd333da8a54756.js',
]:
    result = subprocess.run(['git', 'show', 'ffd1fec:' + filename], capture_output=True)
    c = result.stdout.decode('utf-8')
    print(f'{filename}: {len(c)} bytes')

    # El problema: dentro del SVG hay un comentario con font-family que tiene comillas simples
    # \x3c!-- ... --\x3e  es el comentario JS-escaped
    # Eliminarlo completamente
    new_c = re.sub(r'\\x3c!--.*?--\\x3e', '', c, flags=re.DOTALL)
    
    removed = len(c) - len(new_c)
    print(f'  eliminados {removed} chars del comentario')
    print(f'  Good Father restante: {"Good Father" in new_c}')
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(new_c)
