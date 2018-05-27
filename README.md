installation:
`pip install -r requirements.txt`

to get a bucket: 
`./s3.py get s3://test/ --format >size<`

or to get a sub section of bucket:
`./s3.py get s3://test/subsection* --format >size<`

to list all buckets: 
`./s3.py list --format >size<`

\>size< is optional but must be one of the following:
* b
* kb
* mb
* gb

to list all buckets grouped by region: 
`./s3.py list --format >size< --group`

