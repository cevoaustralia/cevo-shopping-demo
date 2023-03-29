BUCKET="cevo-shopping-demo"
#Path with trailing /
S3PATH="dataset/"
export S3PUBLIC=" --acl public-read"

# Sync product images from Retail Demo Store tutorial bucket to your bucket 
echo " + Copying product images"
aws s3 sync s3://retail-demo-store-code/datasets/1.3/images/ s3://${BUCKET}/${S3PATH}images/ $S3PUBLIC --profile <your-profile-here> || echo "Skipping load of remote image dataset 1.3"
aws s3 sync s3://retail-demo-store-code/datasets/1.4/images/ s3://${BUCKET}/${S3PATH}images/ $S3PUBLIC --profile <your-profile-here> || echo "Skipping load of remote image dataset 1.4"
aws s3 sync datasets/1.4/images/ s3://${BUCKET}/${S3PATH}images/ $S3PUBLIC --profile <your-profile-here> || echo "Skipping load of local image dataset 1.4"
