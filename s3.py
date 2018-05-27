#!/usr/bin/env python3

import sys
import datetime
from collections import defaultdict
import boto3
from s3bucket import S3bucket
if __name__ == "__main__":
    command = sys.argv[1]
    list_buckets = []
    bucket_size_format = "gb"
    if command == 'list':
        list_buckets = S3bucket.get_all_buckets()
    elif command == 'get':
        path = sys.argv[2]
        split_path = path.split('/', 3)
        list_buckets.append(S3bucket.get_bucket(bucket_name=split_path[2], prefix=split_path[3]))

    if  '--format' in sys.argv:
        index_of_format = sys.argv.index('--format') + 1
        bucket_size_format = sys.argv[index_of_format]

    if  '--group' in sys.argv:
            for region, buckets in S3bucket.group_by_region(list_buckets).items():
                print(region)
                for b in buckets:
                    print(b.format(bucket_size_format))
    else:
        for b in list_buckets:
            print(b.format(bucket_size_format))