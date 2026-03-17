import urllib.request

url1 = 'https://mireiacast1.github.io/jupyterlite-s3/extensions/jupydrive-s3/static/956.698b70cd333da8a54756.js'
url2 = url1 + '?v=698b70cd333da8a54756'

for url in [url1, url2]:
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0',
        'Accept': '*/*',
        'Accept-Encoding': 'identity'
    })
    r = urllib.request.urlopen(req)
    c = r.read()
    print(f'URL: {url[-50:]}')
    print(f'  bytes: {len(c)}')
    print(f'  inicio: {repr(c[:60])}')
    print()
