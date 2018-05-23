#!/usr/bin/env python

import sys
import datetime
from collections import defaultdict
import boto3

def list():
    s3 = boto3.resource('s3')
    buckets = []
    for bucket in s3.buckets.all():
        region = get_region(bucket.name)
        objects = get_objects(bucket.name)
        bucket_map = {'name': bucket.name,
                    'bucket_creation_date': bucket.creation_date, 
                    'storage': defaultdict(int), 
                    'count': 0,
                    'last_modified_date': datetime.datetime(1,1,1,tzinfo=datetime.timezone.utc),
                    'region': region,} 
    
        for o in objects:
            bucket_map['count'] = bucket_map['count'] + 1
            # print(o)
            bucket_map['storage'][o['StorageClass']] += o['Size']
            if bucket_map['last_modified_date'] < o['LastModified']:
                bucket_map['last_modified_date'] = o['LastModified']
        buckets.append(bucket_map)
    return buckets

def get_region(bucket_name):
    s3 = boto3.resource('s3')
    return s3.meta.client.get_bucket_location(Bucket=bucket_name)["LocationConstraint"]


def get_objects(bucket_name, prefix=''):
    client = boto3.client('s3')
    # Create a reusable Paginator
    paginator = client.get_paginator('list_objects_v2')
    operation_parameters = {'Bucket': bucket_name,
                            'Prefix': prefix}
    page_iterator = paginator.paginate(**operation_parameters)
    for page in page_iterator:
        for o in page['Contents']:
            yield o

def divisor_map(storage_display_format):
    try:
        return {'b':1,
                'kb': 1024,
                'mb': 1024 * 1024,
                'gb': 1024 * 1024 * 1024,}[storage_display_format]
    except KeyError:
        raise ValueError("{0} is not a valid storage_display_format".format(storage_display_format))


def format_bucket(buckets, storage_display_format='gb'):
    
    division = divisor_map(storage_display_format.lower())
    bucket['bucket_creation_date'] = bucket['bucket_creation_date'].isoformat()
    bucket['last_modified_date'] = bucket['last_modified_date'].isoformat() 
    for key, value in bucket['storage'].items():
        bucket['storage'][key] = "{0} {1}".format(round(value/division, 2),storage_display_format)
    return bucket

def group_by_region(buckets):
    grouped_buckets = defaultdict(list)
    for bucket in buckets:
        region = bucket['region']     
        grouped_buckets[region].append(bucket)
    return grouped_buckets

def configure():
    print('configure')

if __name__ == "__main__":
    # execute only if run as a script
    command = sys.argv[1]
    if command == 'list':
        buckets = list()
        for bucket in buckets:
            if len(sys.argv)>2 and sys.argv[2] != 'group':
                storage_display_format = sys.argv[2]
                bucket  = format_bucket(bucket, storage_display_format)
            else:
                bucket  = format_bucket(bucket)
            
        if 'group' in sys.argv:
            buckets = group_by_region(buckets)
        print("{0}".format(buckets))
    else:
        configure()