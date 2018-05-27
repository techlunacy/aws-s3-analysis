#!/usr/bin/env python

import sys
import datetime
from collections import defaultdict
import boto3

class S3bucket:
    def __init__(self, bucket, prefix = ''):
        self.bucket = bucket
        self.name = bucket.name
        self.creation_date = bucket.creation_date
        self.region = self.get_region()
        self.storage = defaultdict(int)
        self.last_modified_date = datetime.datetime(1,1,1,tzinfo=datetime.timezone.utc)
        self.objects = self.get_objects(prefix)
        self.count = len(self.objects)
        for o in self.objects:
            self.storage[o.storage_class] += o.size
            if self.last_modified_date < o.last_modified:
                self.last_modified_date = o.last_modified            
            

    def __str__(self):
        return "{},{},{},{},{},".format(self.name,
                            self.region,
                            self.count,
                            self.creation_date.isoformat(), 
                            self.last_modified_date.isoformat())

    def get_objects(self, prefix):
        return list(self.bucket.objects.filter(Prefix=prefix.replace("*", "")))

    def get_region(self):
        return self.bucket.meta.client.get_bucket_location(Bucket=self.name)["LocationConstraint"]

    def format(self, bucket_size_format):
        storage_string = ""
        for k,v in self.storage.items():
            value = round(v/self.divisor_map(bucket_size_format), 2)
            storage_string+= "{},{}{},".format(k,value, bucket_size_format)
        return "{},{},{},{},{},{}".format(self.name,
                            self.region,
                            self.count,
                            self.creation_date.isoformat(), 
                            self.last_modified_date.isoformat()
                            ,storage_string)

    @staticmethod
    def divisor_map(storage_display_format):
        try:
            return {'b':1,
                    'kb': 1024,
                    'mb': 1024 * 1024,
                    'gb': 1024 * 1024 * 1024,}[storage_display_format]
        except KeyError:
            raise ValueError("{0} is not a valid storage_display_format".format(storage_display_format))
    
    @staticmethod
    def connection():
        return boto3.resource('s3')
    
    @staticmethod
    def get_all_buckets():
        for b in S3bucket.connection().buckets.all():        
            yield S3bucket(b)
    
    @staticmethod
    def get_bucket(bucket_name, prefix):
        return S3bucket(S3bucket.connection().Bucket(bucket_name), prefix)            


# def divisor_map(storage_display_format):
#     try:
#         return {'b':1,
#                 'kb': 1024,
#                 'mb': 1024 * 1024,
#                 'gb': 1024 * 1024 * 1024,}[storage_display_format]
#     except KeyError:
#         raise ValueError("{0} is not a valid storage_display_format".format(storage_display_format))

# def group_by_region(buckets):
#     grouped_buckets = defaultdict(list)
#     for bucket in buckets:
#         region = bucket['region']     
#         grouped_buckets[region].append(bucket)
#     return grouped_buckets

# def configure():
#     print('configure')

if __name__ == "__main__":
    command = sys.argv[1]
    list_buckets = []
    bucket_size_format = "gb"
    if command == 'list':
        for b in S3bucket.get_all_buckets():
            list_buckets.append(b)
    elif command == 'get':
        path = sys.argv[2]
        split_path = path.split('/', 3)
        list_buckets.append(S3bucket.get_bucket(bucket_name=split_path[2], prefix=split_path[3]))

    if  '--format' in sys.argv:
        index_of_format = sys.argv.index('--format') + 1
        bucket_size_format = sys.argv[index_of_format]

    for b in list_buckets:
        print(b.format(bucket_size_format))