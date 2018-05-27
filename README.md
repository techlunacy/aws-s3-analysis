installation:
`pip install -r requirements.txt`

to get a bucket: 
`./s3.py get s3://test/ --size >size<`

or to get a sub section of bucket:
`./s3.py get s3://test/subsection --size >size<`

to list all buckets: 
`./s3.py list --size >size<`

\>size< is optional but must be one of the following:
* b
* kb
* mb
* gb

to list all buckets grouped by region: 
`./s3.py list --size >size< group`
