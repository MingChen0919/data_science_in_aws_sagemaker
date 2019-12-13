__author__ = 'Ming Chen (ming.chen0919@gmail.com)'
"""
Example use:
    python sync_folder_to_s3.py \
        --aws_profile=[S3_ACCESS_PROFILE] \
        --bucket=sagemaker-[PROJECT-NAME] \
        --local_dir=[FOLDER] \
        --s3_dir=[S3_PATH]
"""

import boto3
import os
import argparse


def sync_dir_to_s3(bucket, local_dir=None, s3_dir=None):
    """Sync a local folder to a S3 Bucket folder

    :param bucket: an S3 Bucket object.
    :param local_dir: the path to the local directory that will be synced to S3
    :param s3_dir: the S3 prefix
    :return:
    """
    if not os.path.isdir(local_dir):
        print('Local directory `{}` does not exist.'.format(local_dir))

    for dirpath, subdirs, files in os.walk(local_dir):
        for file in files:
            source = os.path.join(dirpath, file)
            target = os.path.join(s3_dir, source.replace(local_dir + '/', ''))
            bucket.upload_file(source, target)
            print('Uploaded {} to S3 {}'.format(source, bucket.name))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--aws_profile', type=str,
                        help='Specify an AWS PROFILE which has access permission to S3 service. The AWS PROFILE should be added to ~/.aws/credentials')
    parser.add_argument('--bucket', type=str, help='S3 Bucket name to store the project content')
    parser.add_argument('--local_dir', type=str, help='path ti local directory that will be synced to S3')
    parser.add_argument('--s3_dir', type=str, help='S3 directory to which the local folder will be synced')

    args = parser.parse_args()

    os.environ['AWS_PROFILE'] = args.aws_profile

    # create an S3 client and specify a region
    s3_client = boto3.client('s3', region_name='us-east-2')
    all_buckets = s3_client.list_buckets()['Buckets']
    all_buckets = [b['Name'] for b in all_buckets]

    # create a Bucket for this project if it doesn't exist
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(args.bucket)
    if args.bucket not in all_buckets:
        bucket.create(
            ACL='private',
            CreateBucketConfiguration={
                'LocationConstraint': 'us-east-2'
            }
        )
        print('Created S3 Bucket {}'.format(args.bucket))

    sync_dir_to_s3(bucket, local_dir=args.local_dir, s3_dir=args.s3_dir)
