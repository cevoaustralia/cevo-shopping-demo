import boto3
from generators.generate_items_and_interactions_personalize import generate_interactions

bucket = "cevo-shopping-demo"
interactions_filename = "./generators/interactions.csv"

generate_interactions()

boto3.Session(profile_name=<aws-profile-replace-me>, region_name="ap-southeast-2").resource(
    "s3"
).Bucket(bucket).Object(interactions_filename).upload_file(interactions_filename)
