import boto3
from moto import mock_s3
import pytest
from s3 import S3bucket
import datetime
@mock_s3
def test_all_buckets_are_returned():
    conn = boto3.resource('s3')
    # We need to create the bucket since this is all in Moto's 'virtual' AWS account
    for i in range(10):
        conn.create_bucket(Bucket='mybucket{}'.format(i))
    assert len(list(S3bucket.get_all_buckets())) == 10

@mock_s3
def test_all_buckets_have_the_right_count():
    conn = boto3.resource('s3')
    # We need to create the bucket since this is all in Moto's 'virtual' AWS account
    for i in range(10):
        conn.create_bucket(Bucket='mybucket{}'.format(i))
        for j in range(10):
            # conn.Bucket('mybucket{}'.format(i)).upload_fileobj('/tmp/mybucket{}'.format(j), tempfile.TemporaryFile())
            conn.meta.client.put_object(Bucket='mybucket{}'.format(i), Key='tmp/mybucket{}'.format(j), Body='/tmp/mybucket{}'.format(j))   
        
        for b in S3bucket.get_all_buckets():
            assert b.count == 10
            assert b.count == 10
            assert b.last_modified_date > datetime.datetime(1,1,1,tzinfo=datetime.timezone.utc)                       
            assert len(b.storage.keys()) > 0
            assert sum(b.storage.values()) > 0

def test_divisor_map():

    assert S3bucket.divisor_map('mb') == 1024 * 1024  
    assert S3bucket.divisor_map('gb') == 1024 * 1024 * 1024
    assert S3bucket.divisor_map('GB') == 1024 * 1024 * 1024
    with pytest.raises(ValueError):
        S3bucket.divisor_map('XB')
