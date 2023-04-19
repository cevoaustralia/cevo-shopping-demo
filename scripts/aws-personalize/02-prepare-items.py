import boto3
from generators.generate_items_and_interactions_personalize import generate_user_items

bucket = "cevo-shopping-demo"
products_filename = "./generators/items.csv"

generate_user_items()

boto3.Session(profile_name=<aws-profile-replace-me>, region_name="ap-southeast-2").resource(
    "s3"
).Bucket(bucket).Object(products_filename).upload_file(products_filename)
