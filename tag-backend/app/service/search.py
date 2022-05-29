import json
import boto3

f = boto3.client('lambda')


def query(model):
    if(model.tags is not None and len(model.tags) > 0):
        return query_by_tag(model.tags)
    else:
        return query_by_url(model.url)


def query_by_image(key):
    event = {
        "Records": [
            {
                "s3": {
                    "object": {
                        "key": key,
                    }
                }
            }
        ]
    }
    response = f.invoke(FunctionName='process_img_tag',
                        Payload=json.dumps(event))
    value = response['Payload'].read().decode('utf-8')
    return json.loads(value)


def query_by_url(url):
    response = f.invoke(FunctionName='query_lambda',
                        Payload=json.dumps({'type': 'url', 'data': url}))
    print(response)
    value = response['Payload'].read().decode('utf-8')
    return json.loads(value)


def query_by_tag(tags):
    response = f.invoke(FunctionName='query_lambda',
                        Payload=json.dumps({'type': 'tag', 'data': tags}))
    print(response)
    value = response['Payload'].read().decode('utf-8')
    return json.loads(value)

