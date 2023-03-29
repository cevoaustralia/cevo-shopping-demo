import boto3

bucket = "cevo-shopping-demo"
products_filename = "../../generators/items.csv"

boto3.Session(profile_name=<aws-profile-replace-me>, region_name="ap-southeast-2").resource(
    "s3"
).Bucket(bucket).Object(products_filename).upload_file(products_filename)
