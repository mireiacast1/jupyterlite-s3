c = open('extensions/jupydrive-s3/static/956.698b70cd333da8a54756.js', encoding='utf-8').read()
i = c.find('svgstr')
print("chars:", [(j, repr(ch)) for j, ch in enumerate(c[i:i+15])])

# El SVG empieza despues de svgstr: y un delimitador
# Buscar desde svgstr hasta el cierre del svg
svg_start = c.find('<svg', i)
svg_end = c.find('</svg>', svg_start) + len('</svg>')
svg_content = c[svg_start:svg_end]
print("svg tiene comillas dobles:", svg_content.count('"'))
print("svg preview:", repr(svg_content[:100]))
