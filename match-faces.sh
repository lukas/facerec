aws s3 cp $1 s3://doorcamera > output
aws rekognition search-faces-by-image --collection-id "friends" --image "{\"S3Object\":{\"Bucket\":\"doorcamera\",\"Name\":\"$1\"}}"
