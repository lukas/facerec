aws s3 cp $1 s3://doorcamera > output
aws rekognition detect-faces --attributes "ALL" --image "{\"S3Object\":{\"Bucket\":\"doorcamera\",\"Name\":\"$1\"}}"
