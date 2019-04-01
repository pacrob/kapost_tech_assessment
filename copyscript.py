import boto3
import sys
import bucket_actions as ba

if len(sys.argv) != 4:
    print("Usage: python3 copyscript.py <from-bucket> <to-bucket> <threshold>")
    exit(0)

s3_resource = boto3.resource('s3')

from_bucket = sys.argv[1]
to_bucket = sys.argv[2]
threshold = float(sys.argv[3])


copy_count = ba.copy_to_bucket_if_larger_than(s3_resource, from_bucket,
                                              to_bucket, threshold)

print(f"Copied {copy_count} files")
