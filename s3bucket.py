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

    def __json__(self):
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
    
    def formatted_dict(self, bucket_size_format):
        dictionary = {}
        storage_dict = {}
        for k,v in self.storage.items():
            value = round(v/self.divisor_map(bucket_size_format), 2)
            storage_dict[k] = "{}{}".format(value, bucket_size_format)
        dictionary['name'] = str(self.name),
        dictionary['region'] = str(self.region),
        dictionary['count'] = self.count,
        dictionary['creation_date'] = str(self.creation_date.isoformat()), 
        dictionary['last_modified_date'] = str(self.last_modified_date.isoformat())
        dictionary['storage'] = storage_dict                            
        return dictionary
    @staticmethod
    def divisor_map(storage_display_format):
        try:
            return {'b':1,
                    'kb': 1024,
                    'mb': 1024 * 1024,
                    'gb': 1024 * 1024 * 1024,}[storage_display_format.lower()]
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

    @staticmethod
    def group_by_region(buckets):
        grouped_buckets = dict()
        for b in buckets:
            region = b.region     
            grouped_buckets.setdefault(region, []).append(b)
        return grouped_buckets
