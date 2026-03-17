import re, subprocess

# usar el original de ffd1fec (primer commit del archivo)
result = subprocess.run(['git', 'show', 'ffd1fec:extensions/jupydrive-s3/static/956.698b70cd333da8a54756.js'], capture_output=True)
c = result.stdout.decode('utf-8')
print('original bytes:', len(c))

# eliminar comentario HTML escapado
c = re.sub(r'\\x3c!--.*?--\\x3e', '', c, flags=re.DOTALL)

# reemplazar svgstr:'...' por svgstr:'' - eliminar todo el SVG
new_c = re.sub(r"svgstr:'.*?'(?=[,}])", "svgstr:''", c, flags=re.DOTALL)
print('nuevo bytes:', len(new_c))
print('svgstr vacios:', new_c.count("svgstr:''"))

for filename in [
    'extensions/jupydrive-s3/static/956.698b70cd333da8a54755.js',
    'extensions/jupydrive-s3/static/956.698b70cd333da8a54756.js',
    'extensions/jupydrive-s3/static/956.698b70cd333da8a54757.js',
]:
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        f.write(new_c)
    r = subprocess.run(['node', '--check', filename], capture_output=True, text=True)
    status = 'OK' if r.returncode == 0 else r.stderr.split('\n')[2] if r.stderr else 'ERROR'
    print(f'{filename[-20:]}: {status}')
