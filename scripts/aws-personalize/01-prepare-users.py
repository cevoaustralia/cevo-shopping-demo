import pandas as pd
import boto3
from generators.generate_users_json import generate_users_json

bucket = "cevo-shopping-demo"
users_filename = "./generators/users.csv"

generate_users_json()

boto3.Session(profile_name=<aws-profile-replace-me>, region_name="ap-southeast-2").resource(
    "s3"
).Bucket(bucket).Object(users_filename).upload_file(users_filename)
