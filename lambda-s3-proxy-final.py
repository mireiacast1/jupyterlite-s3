import json
import boto3
from botocore.exceptions import ClientError

CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, PUT, POST, DELETE, HEAD, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Amz-Date, X-Amz-Security-Token, X-Amz-User-Agent, X-Amz-Content-Sha256, X-Amz-Access-Key-Id, X-Amz-Secret-Access-Key, X-Amz-Checksum-Mode',
    'Access-Control-Expose-Headers': 'ETag, Content-Length, Content-Type'
}

def lambda_handler(event, context):
    method = event['httpMethod']
    path = event.get('pathParameters', {}).get('proxy', '')
    query = event.get('queryStringParameters', {}) or {}
    headers = {k.lower(): v for k, v in event.get('headers', {}).items()}
    
    if method == 'OPTIONS':
        return {'statusCode': 200, 'headers': CORS_HEADERS, 'body': ''}
    
    access_key = headers.get('x-amz-access-key-id')
    secret_key = headers.get('x-amz-secret-access-key')
    session_token = headers.get('x-amz-security-token')
    
    if access_key and secret_key:
        s3 = boto3.client('s3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            aws_session_token=session_token
        )
    else:
        s3 = boto3.client('s3')
    
    parts = path.split('/', 1)
    bucket = parts[0]
    key = parts[1] if len(parts) > 1 else ''
    
    try:
        if method == 'GET':
            if 'list-type' in query:
                response = s3.list_objects_v2(
                    Bucket=bucket,
                    Prefix=query.get('prefix', ''),
                    Delimiter=query.get('delimiter', '')
                )
                return {
                    'statusCode': 200,
                    'headers': {**CORS_HEADERS, 'Content-Type': 'application/xml'},
                    'body': format_list_response(response)
                }
            else:
                obj = s3.get_object(Bucket=bucket, Key=key)
                return {
                    'statusCode': 200,
                    'headers': {**CORS_HEADERS, 'Content-Type': obj.get('ContentType', 'application/octet-stream'), 'ETag': obj['ETag']},
                    'body': obj['Body'].read().decode('utf-8')
                }
        
        elif method == 'PUT':
            s3.put_object(Bucket=bucket, Key=key, Body=event.get('body', ''))
            return {'statusCode': 200, 'headers': CORS_HEADERS, 'body': ''}
        
        elif method == 'DELETE':
            s3.delete_object(Bucket=bucket, Key=key)
            return {'statusCode': 204, 'headers': CORS_HEADERS, 'body': ''}
        
        elif method == 'HEAD':
            obj = s3.head_object(Bucket=bucket, Key=key)
            return {
                'statusCode': 200,
                'headers': {**CORS_HEADERS, 'Content-Type': obj.get('ContentType', 'application/octet-stream'), 'ETag': obj['ETag']},
                'body': ''
            }
    
    except ClientError as e:
        return {
            'statusCode': 404 if e.response['Error']['Code'] == 'NoSuchKey' else 500,
            'headers': CORS_HEADERS,
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': CORS_HEADERS,
            'body': json.dumps({'error': str(e)})
        }

def format_list_response(response):
    xml = '<?xml version="1.0" encoding="UTF-8"?><ListBucketResult>'
    for item in response.get('Contents', []):
        xml += f'<Contents><Key>{item["Key"]}</Key><Size>{item["Size"]}</Size><LastModified>{item["LastModified"].isoformat()}</LastModified></Contents>'
    for prefix in response.get('CommonPrefixes', []):
        xml += f'<CommonPrefixes><Prefix>{prefix["Prefix"]}</Prefix></CommonPrefixes>'
    xml += '</ListBucketResult>'
    return xml
