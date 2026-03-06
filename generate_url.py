"""Module for obtaining temporary AWS credentials using SSO."""
import boto3
from botocore.exceptions import BotoCoreError, ClientError


def get_temporary_credentials():
    """Obtain temporary AWS credentials using SSO profile."""
    try:
        session = boto3.Session(profile_name='lakehouse-dev')
        credentials = session.get_credentials()

        if credentials is None:
            print("No se pudieron obtener credenciales. Ejecuta: aws sso login --profile lakehouse-dev")
            return None

        return {
            'AccessKeyId': credentials.access_key,
            'SecretAccessKey': credentials.secret_key,
            'SessionToken': credentials.token
        }

    except (BotoCoreError, ClientError) as e:
        print(f"Error obteniendo credenciales: {str(e)}")
        print("Ejecuta: aws sso login --profile lakehouse-dev")
        return None


def generate_url(s3uri, credentials):
    """Genera una URL para acceder a JupyterLite con las credenciales proporcionadas."""
    import urllib.parse

    if not s3uri.startswith('s3://'):
        raise ValueError('Invalid s3uri')

    s3uri_parts = s3uri[5:].split('/', 1)
    bucket = s3uri_parts[0]
    root = s3uri_parts[1] if len(s3uri_parts) > 1 else ''

    jupyterlite_url = 'https://mireiacast1.github.io/jupyterlite-s3/lab/index.html'

    query_params = {
        'bucket': bucket,
        'root': root,
        'accessKeyId': credentials['AccessKeyId'],
        'secretAccessKey': credentials['SecretAccessKey'],
        'sessionToken': credentials['SessionToken'],
        'region': 'eu-central-1'
    }

    return f"{jupyterlite_url}?{urllib.parse.urlencode(query_params)}"


if __name__ == "__main__":
    import webbrowser
    
    creds = get_temporary_credentials()
    if creds:
        s3uri = 's3://amazon-sagemaker-756160875065-eu-central-1-92b9dc596c3a/dzd-5hy484830n1i2z/6e7tsaqeulkl1n/shared'
        url = generate_url(s3uri, creds)
        print(f"Opening: {url}")
        webbrowser.open(url)
