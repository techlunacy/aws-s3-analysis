from flask import Flask
from flask import jsonify
from s3bucket import S3bucket
import json
if __name__ == '__main__':
    app = Flask(__name__)

    @app.route("/list", defaults={'sizeformat': 'gb'})
    @app.route('/list/<sizeformat>')
    def list(sizeformat):
        buckets = []
        for b in S3bucket.get_all_buckets():
            buckets.append(b.formatted_dict(sizeformat))
        return jsonify(buckets)

    @app.route("/group", defaults={'sizeformat': 'gb'})
    @app.route('/group/<sizeformat>')
    def group(sizeformat):
        original_group = S3bucket.group_by_region(S3bucket.get_all_buckets())    
        buckets = dict.fromkeys(original_group.keys(),[])
        for region, b in original_group.items():
            for bucket in b:
                buckets[region].append(bucket.formatted_dict(sizeformat))
        return jsonify(buckets)    

    @app.route('/get/<sizeformat>/<bucketname>', defaults={'prefix': ''})
    @app.route('/get/<sizeformat>/<bucketname>/<path:prefix>')
    def get(sizeformat, bucketname, prefix):
        return jsonify(S3bucket.get_bucket(bucket_name=bucketname, prefix=prefix).formatted_dict(sizeformat))    