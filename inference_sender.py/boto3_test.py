import boto3


s3 = boto3.resource('s3')

for bucket in s3.buckets.all():
    print(bucket.name)

# Upload a new file
# with open('test.jpg', 'rb') as data:
#     s3.Bucket('amzn-s3-demo-bucket').put_object(Key='test.jpg', Body=data)