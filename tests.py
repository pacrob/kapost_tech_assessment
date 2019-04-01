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

        # can create test file of specified size in MB
        fileA_size_MB = 2
        fileB_size_MB = 4
        fileC_size_MB = 5
        fileA = 'fileA'
        fileB = 'fileB'
        fileC = 'fileC'
        file_content = 'z'

        ba.create_temp_file(fileA_size_MB, fileA, file_content)
        ba.create_temp_file(fileB_size_MB, fileB, file_content)
        ba.create_temp_file(fileC_size_MB, fileC, file_content)

        new_file_size = os.stat(fileA).st_size    
        fileA_size_in_bytes = fileA_size_MB * ba.MBYTES
        self.assertEqual(fileA_size_in_bytes, new_file_size)

        # can upload file to bucket and make sure its there

        bucketA_objectA = s3_resource.Object(
                bucket_name=bucketA_name, key=fileA)
        bucketA_objectB = s3_resource.Object(
                bucket_name=bucketA_name, key=fileB)
        bucketA_objectC = s3_resource.Object(
                bucket_name=bucketA_name, key=fileC)

        bucketA_objectA.upload_file(fileA)
        bucketA_objectB.upload_file(fileB)
        bucketA_objectC.upload_file(fileC)

        file_list = ba.get_files_in_bucket(s3_resource, bucketA_name)

        self.assertIn(fileA, file_list)
        self.assertIn(fileB, file_list)
        self.assertIn(fileC, file_list)

        # can get size of a file in a bucket

        retrieved_fileA_size = ba.get_file_size(s3_resource, bucketA_name, fileA)
        self.assertEqual(retrieved_fileA_size, fileA_size_MB * ba.MBYTES)
        
        # can copy a file from one bucket to another

        bucketB_name, bucketB_instance = ba.create_bucket(
                bucket_prefix='bucket-b',
                s3_connection=s3_resource)
        
        ba.copy_to_bucket(s3_resource, bucketA_name, bucketB_name, fileA)

        file_list = ba.get_files_in_bucket(s3_resource, bucketB_name)
        self.assertIn(fileA, file_list)

        # can copy all files larger than a given size in MB 
        # from one bucket to another

        ba.empty_bucket(s3_resource, bucketB_name)

        
        files_in_bucketA = ba.get_files_in_bucket(s3_resource, bucketA_name)
        ## will move files B and C over to bucketB, but not fileA
        ## by looking for files larger than 3 MB
        target_size = 3

        ba.copy_to_bucket_if_larger_than(s3_resource, bucketA_name,
                                         bucketB_name, target_size)

        files_in_bucketB = ba.get_files_in_bucket(s3_resource, bucketB_name)

        self.assertIn(fileB, files_in_bucketB)
        self.assertIn(fileC, files_in_bucketB)
        self.assertNotIn(fileA, files_in_bucketB)

        # empty and delete test buckets

        ba.empty_bucket(s3_resource, bucketA_name)
        s3_resource.Bucket(bucketA_name).delete()
        ba.empty_bucket(s3_resource, bucketB_name)
        s3_resource.Bucket(bucketB_name).delete()

if __name__ == '__main__':
    unittest.main()
