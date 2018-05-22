import boto3

client = boto3.client('ssm',
                      region_name='eu-west-1')


def get_parameters_by_path(root_path):
    response = client.get_parameters_by_path(
        Path=root_path,
        Recursive=True,
        WithDecryption=True
    )
    secret_store = {}
    for secret in response['Parameters']:
        secret_store[secret['Name'].split('/')[-1]] = secret['Value']

    return secret_store