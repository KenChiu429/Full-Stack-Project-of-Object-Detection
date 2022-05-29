from uuid import uuid4
import boto3

s3 = boto3.client('s3')


def upload_image(file, suffix):
    try:
        key = str(uuid4()).replace('-', '') + '.' + suffix
        s3.put_object(Bucket='image-tag-bucket', Body=file, Key=key)
        return {'isSuccess': True, 'key': key}
    except Exception as e:
        print(e)
        return {'isSuccess': False, 'key': key}
