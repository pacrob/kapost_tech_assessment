# using some code from https://realpython.com/python-boto3-aws-s3/


import boto3
import uuid

MBYTES = 1000000

def create_bucket_name(bucket_prefix):
    return ''.join([bucket_prefix, str(uuid.uuid4())])

def create_bucket(bucket_prefix, s3_connection):
    session = boto3.session.Session()
    current_region = session.region_name
    bucket_name = create_bucket_name(bucket_prefix)
    bucket_response = s3_connection.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': current_region})
    print(bucket_name, current_region)
    return bucket_name, bucket_response

def create_temp_file(size, file_name, file_content):
    size_in_bytes = int(size * MBYTES)
    with open(file_name, 'w') as f:
        f.write(str(file_content) * size_in_bytes)
    return file_name

def get_files_in_bucket(s3_connection, bucket_name):
    file_list = []
    for file in s3_connection.Bucket(bucket_name).objects.all():
        file_list.append(file.key)
    return file_list


def get_file_size(s3_connection, bucket_name, file_name):
    return s3_connection.Bucket(bucket_name).Object(file_name).content_length

def copy_to_bucket(s3_connection, bucket_from_name, bucket_to_name, file_name):
    copy_source = {
            'Bucket': bucket_from_name,
            'Key': file_name
            }
    s3_connection.Object(bucket_to_name, file_name).copy(copy_source)


