#! /bin/sh

usage()
{
    echo 'Usage: add-face.sh <url> <name>'
    echo 'Downloads a picture from url and trains Amazon Rekognition to'
    echo 'recognize the face with given name'
    echo 'Example: '
    echo '  wget -O lukas.jpg https://avatars0.githubusercontent.com/u/29?v=3&s=400'
    echo '  ./add-face.sh lukas.jpg lukas'
    exit
}

if [ "$#" -ne 2 ]
then
    usage
fi


aws s3 cp $1 s3://doorcamera > output
aws rekognition index-faces \
  --image "{\"S3Object\":{\"Bucket\":\"doorcamera\",\"Name\":\"$1\"}}" --collection-id "friends" --detection-attributes "ALL" --external-image-id "$2" 
