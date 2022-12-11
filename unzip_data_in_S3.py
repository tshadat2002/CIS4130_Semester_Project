#Replace Variables as Necessary and make sure to install libraries into instance as necessary as well
import zipfile
import boto3
from io import BytesIO
bucket="project-data-XX"   # Put your bucket name here
zipfile_to_unzip="archive.zip"   # Put the name of your Zip file here
s3_client = boto3.client('s3', use_ssl=False)
s3_resource = boto3.resource('s3')

zip_obj = s3_resource.Object(bucket_name=bucket, key=zipfile_to_unzip)
buffer = BytesIO(zip_obj.get()["Body"].read())
z = zipfile.ZipFile(buffer)
for filename in z.namelist():    # Loop through all of the files contained in the Zip archive
    print('Working on ' + filename)
    # Unzip the file and write it back to S3 in the same bucket
    s3_resource.meta.client.upload_fileobj(z.open(filename),Bucket=bucket,Key=f'{filename}')
