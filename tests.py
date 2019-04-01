import unittest
import boto3
import bucket_actions as ba
import os

class BucketTests(unittest.TestCase):

    def test_copy_bucket_files(self):

        s3_resource = boto3.resource('s3')

        # can create new bucket name w/ unique name ending in a uuid4

        bucket_prefix = 'bucket'
        bucket_name = ba.create_bucket_name(bucket_prefix)
        self.assertTrue(bucket_name.startswith(bucket_prefix))
        self.assertEqual(len(bucket_name), len(bucket_prefix) + 36)

        # can create bucket

        bucketA_name, bucketA_instance = ba.create_bucket(
                bucket_prefix='bucket-a',
                s3_connection=s3_resource)

        self.assertIsNotNone(bucketA_name)
        self.assertIsNotNone(bucketA_instance)

        # can create test file of specified size
        fileA_size = 50
        file_content = 'z'
        fileA = 'fileA'

        ba.create_temp_file(fileA_size, fileA, file_content)

        new_file_size = os.stat(fileA).st_size    
        self.assertEqual(fileA_size, new_file_size)

        # can upload file to bucket and make sure its there

        bucketA_object = s3_resource.Object(
                bucket_name=bucketA_name, key=fileA)

        bucketA_object.upload_file(fileA)

        file_list = ba.get_files_in_bucket(s3_resource, bucketA_name)

        self.assertIn(fileA, file_list)

        # can get size of a file in a bucket

        retrieved_fileA_size = ba.get_file_size(s3_resource, bucketA_name, fileA)
        self.assertEqual(retrieved_fileA_size, fileA_size)
        
        # can copy a file from one bucket to another

        bucketB_name, bucketB_instance = ba.create_bucket(
                bucket_prefix='bucket-b',
                s3_connection=s3_resource)
        
        ba.copy_to_bucket(s3_resource, bucketA_name, bucketB_name, fileA)

        file_list = ba.get_files_in_bucket(s3_resource, bucketB_name)
        self.assertIn(fileA, file_list)



        # can copy all files larger than a given size in MB 
        # from one bucket to another

        fileB = 'fileB'
        ba.create_temp_file(100, fileB, 'z')
        bucketA_object.upload_file(fileB)
        fileC = 'fileC'
        ba.create_temp_file(150, fileC, 'z')
        bucketA_object.upload_file(fileC)

        # empty and delete test buckets

        bucketA_bucket = s3_resource.Bucket(bucketA_name)
        for key in bucketA_bucket.objects.all():
            key.delete()
        bucketA_bucket.delete()
        bucketB_bucket = s3_resource.Bucket(bucketB_name)
        for key in bucketB_bucket.objects.all():
            key.delete()
        bucketB_bucket.delete()

if __name__ == '__main__':
    unittest.main()
