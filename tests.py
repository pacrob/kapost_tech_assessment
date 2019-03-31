import unittest
import boto3
import bucket_actions as ba


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

        # can create test file

            
        # can upload file to bucket

        


        # can get sizes files in a bucket



        # can copy a file from one bucket to another



        # can copy all files larger than a given size in MB 
        # from one bucket to another

if __name__ == '__main__':
    unittest.main()
