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

def empty_bucket(s3_connection, bucket_name):
    for key in s3_connection.Bucket(bucket_name).objects.all():
        key.delete()

def copy_to_bucket_if_larger_than(s3_connection, from_bucket, to_bucket, size):
    from_files = get_files_in_bucket(s3_connection, from_bucket)
    copied_files_count = 0
    for file_name in from_files:
        if (get_file_size(s3_connection, from_bucket, file_name) / MBYTES) > size:
            copied_files_count += 1
            copy_to_bucket(s3_connection, from_bucket, to_bucket, file_name)
    return copied_files_count

