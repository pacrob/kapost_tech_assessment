# using some code from https://realpython.com/python-boto3-aws-s3/


import boto3
import uuid

s3_resource = boto3.resource('s3')


def create_bucket_name(bucket_prefix):
    return ''.join([bucket_prefix, str(uuid.uuid4())])

def create_bucket(bucket_prefix, s3_connection):
    session = boto3.session.Session()
    current_region = session.region_name
    bucket_name = create_bucket_name(bucket_prefix)
    bucket_response = s3_connection.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': current_region})
    print(bucket_name, current_region)
    return bucket_name, bucket_response

def create_temp_file(size, file_name, file_content):
    random_file_name = ''.join([str(uuid.uuid4().hex[:6]), file_name])
    with open(random_file_name, 'w') as f:
        f.write(str(file_content) * size)
    return random_file_name

def copy_to_bucket(bucket_from_name, bucket_to_name, file_name):
    copy_source = {
            'Bucket': bucket_from_name,
            'Key': file_name
            }
    s3_resource.Object(bucket_to_name, file_name).copy(copy_source)


