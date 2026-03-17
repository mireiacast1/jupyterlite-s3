import urllib.request, re, gzip

req = urllib.request.Request(
    'https://mireiacast1.github.io/jupyterlite-s3/extensions/jupydrive-s3/static/956.698b70cd333da8a54757.js?v=698b70cd333da8a54757',
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip'
    }
)
r = urllib.request.urlopen(req)
raw = r.read()
print('raw bytes:', len(raw))
print('content-encoding:', r.headers.get('Content-Encoding'))

# descomprimir si es gzip
if r.headers.get('Content-Encoding') == 'gzip':
    c = gzip.decompress(raw).decode('utf-8')
else:
    c = raw.decode('utf-8')

print('decompressed bytes:', len(c))
print('pos 21680-21730:', repr(c[21680:21730]))

# buscar entidades HTML
entities = re.findall(r'&[a-zA-Z#0-9]+;', c)
print('entidades HTML:', entities[:10])

# buscar el problema en pos 21706
print('char 21706:', repr(c[21706]), ord(c[21706]))
