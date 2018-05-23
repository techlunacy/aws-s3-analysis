#!/usr/bin/env python

import sys
import datetime
import boto3

def list():
    s3 = boto3.resource('s3')

    for bucket in s3.buckets.all():
        objects = get_objects(bucket.name)
        bucket_map = {'name': bucket.name,
                    'creation_date': bucket.creation_date, 
                    'object_size': 0, 
                    'count': 0,
                    'last_modified_date': datetime.datetime(1,1,1,tzinfo=datetime.timezone.utc)} 
     
        for o in objects:
            bucket_map['count'] = bucket_map['count'] + 1
            # print(o)
            bucket_map['object_size'] += o['Size']
            if bucket_map['last_modified_date'] < o['LastModified']:
                bucket_map['last_modified_date'] = o['LastModified']
        print("{0}".format(bucket_map))



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

def configure():
    print('configure')

if __name__ == "__main__":
    # execute only if run as a script
    command = sys.argv[1]
    if command == 'list':
        list()
    else:
        configure()