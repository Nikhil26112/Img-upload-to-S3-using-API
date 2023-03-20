from flask import Flask, request
import boto3

s3_client = boto3.client('s3', region_name='ap-south-1')

bucket_name = 'nikhil-chauhan'

# Check if the bucket already exists
response = s3_client.list_buckets()
if bucket_name not in [bucket['Name'] for bucket in response['Buckets']]:
    # Create the bucket if it doesn't exist
    s3_client.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint': 'ap-south-1'
        }
    )

app = Flask(__name__)


@app.route('/upload_image', methods=['POST'])
def upload_image():
    # Get the uploaded image file
    file = request.files['image']

    # Upload the image file to your S3 bucket
    s3_client.upload_fileobj(
        file,
        bucket_name,
        file.filename
    )
    return 'Image uploaded successfully!'


if __name__ == '__main__':
    app.run()

# To check use this command from local computer
# curl -X POST -F 'image=@/home/nikhil/Desktop/Project/Samajh-AI-Assessment/image.png' http://localhost:5000/upload_image
