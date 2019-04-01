import boto3
import sys
import bucket_actions as ba

# check correct number of args
if len(sys.argv) != 4:
    print("Usage: python3 copyscript.py <from-bucket> <to-bucket> <threshold>")
    exit(0)

# check threshold is a number
try:
    float(sys.argv[3])
except:
    print("threshold must be type int or float")
    exit(1)

s3_resource = boto3.resource('s3')
from_bucket = sys.argv[1]
to_bucket = sys.argv[2]
threshold = float(sys.argv[3])

# validate bucket names

if (s3_resource.Bucket(from_bucket) in s3_resource.buckets.all()) == False:
    print("from-bucket name does not exist")
    exit(1)

if (s3_resource.Bucket(to_bucket) in s3_resource.buckets.all()) == False:
    print("to-bucket name does not exist")
    exit(1)

# go ahead and copy

copy_count = ba.copy_to_bucket_if_larger_than(s3_resource, from_bucket,
                                              to_bucket, threshold)

print(f"Copied {copy_count} files")
