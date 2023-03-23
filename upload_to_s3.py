from werkzeug.utils import secure_filename
from flask import Flask, render_template, request
import boto3
app = Flask(__name__)

s3_client = boto3.client('s3', region_name='ap-south-1')

BUCKET_NAME = 'nikhil--chauhan'

# Check if the bucket already exists
response = s3_client.list_buckets()
if BUCKET_NAME not in [bucket['Name'] for bucket in response['Buckets']]:
    # Create the bucket if it doesn't exist
    s3_client.create_bucket(
        Bucket=BUCKET_NAME,
        CreateBucketConfiguration={
            'LocationConstraint': 'ap-south-1'
        }
    )


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/upload', methods=['post'])
def upload():
    if request.method == 'POST':
        img = request.files['file']
        if img:
            filename = secure_filename(img.filename)
            img.save(filename)
            s3_client.upload_file(
                Bucket=BUCKET_NAME,
                Filename=filename,
                Key=filename
            )
            msg = "Upload Done ! "

    return render_template("index.html", msg=msg)


if __name__ == "__main__":

    app.run(debug=True)
