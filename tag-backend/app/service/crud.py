import json
import boto3

f = boto3.client('lambda')


def delete_file(url):
    try:
        f.invoke(FunctionName='delete_lambda',
                 Payload=json.dumps({'url': url}))
        return True
    except Exception as e:
        print(e)
        return False


def update_tag(model):
    try:
        f.invoke(FunctionName='update_lambda',
                 Payload=json.dumps(
                     {
                         'url': model.url,
                         'tags': list(model.tags),
                         'type': model.type
                     }
                 )
                 )
        return True
    except Exception as e:
        print(e)
        return False
