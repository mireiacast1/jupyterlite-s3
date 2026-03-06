import json
import urllib.parse

def lambda_handler(event, context):
    params = event.get('queryStringParameters', {})
    
    s3uri = params.get('s3uri', '')
    access_key = params.get('accessKeyId', '')
    secret_key = params.get('secretAccessKey', '')
    session_token = params.get('sessionToken', '')
    
    # Parsear s3uri: s3://bucket/path/to/folder
    if not s3uri.startswith('s3://'):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid s3uri'})
        }
    
    s3uri_parts = s3uri[5:].split('/', 1)
    bucket = s3uri_parts[0]
    root = s3uri_parts[1] if len(s3uri_parts) > 1 else ''
    
    # Construir URL de JupyterLite
    jupyterlite_url = 'https://mireiacast1.github.io/jupyterlite-clean/lab/index.html'
    
    query_params = {
        'bucket': bucket,
        'root': root,
        'accessKeyId': access_key,
        'secretAccessKey': secret_key,
        'sessionToken': session_token,
        'region': 'eu-central-1'
    }
    
    url = f"{jupyterlite_url}?{urllib.parse.urlencode(query_params)}"
    
    return {
        'statusCode': 302,
        'headers': {
            'Location': url
        }
    }
