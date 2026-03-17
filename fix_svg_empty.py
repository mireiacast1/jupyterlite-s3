import re, subprocess

for filename in [
    'extensions/jupydrive-s3/static/956.698b70cd333da8a54755.js',
    'extensions/jupydrive-s3/static/956.698b70cd333da8a54756.js',
]:
    result = subprocess.run(['git', 'show', 'HEAD~4:' + filename], capture_output=True)
    c = result.stdout.decode('utf-8')
    print(f'{filename}: original {len(c)} bytes')

    # reemplazar svgstr:'<svg...>' por svgstr:''
    new_c = re.sub(r"svgstr:'.*?'(?=[,}])", "svgstr:''", c, flags=re.DOTALL)
    
    count = c.count("svgstr:'") 
    print(f'  SVGs eliminados: {count}')
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(new_c)
    print(f'  nuevo tamaño: {len(new_c)} bytes')
