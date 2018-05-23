#!/usr/bin/env python

import sys
import boto3

def list():
    s3 = boto3.resource('s3')

    for bucket in s3.buckets.all():
        objects = get_objects(bucket.name)
        bucket_map = {'name': bucket.name,
                    'creation_date': bucket.creation_date, 
                    'object_size': 0, 
                    'size': len(objects),}       
        for o in objects:
            bucket_map['object_size'] += o['Size'] 
        
        print("{0}".format(bucket_map))



def get_objects(bucket_name, prefix=''):
    
    client = boto3.client('s3')
    # Create a reusable Paginator
    paginator = client.get_paginator('list_objects_v2')
    operation_parameters = {'Bucket': bucket_name,
                            'Prefix': prefix}
    page_iterator = paginator.paginate(**operation_parameters)
    objects = []
    for page in page_iterator:
        objects += page['Contents']
    return objects
def configure():
    print('configure')

if __name__ == "__main__":
    # execute only if run as a script
    command = sys.argv[1]
    if command == 'list':
        list()
    else:
        configure()