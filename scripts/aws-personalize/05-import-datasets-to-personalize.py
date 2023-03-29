import json
import pandas as pd
import boto3
import uuid

bucket = "cevo-shopping-demo"
users_filename = "users.csv"
items_filename = "items.csv"
interactions_filename = "interactions.csv"

s3 = boto3.Session(
    profile_name="cevo-joreyes-dev", region_name="ap-southeast-2"
).client("s3")

response = s3.get_bucket_policy(Bucket=bucket)
print(json.dumps(json.loads(response["Policy"]), indent=2))

iam = boto3.Session(
    profile_name="cevo-joreyes-dev", region_name="ap-southeast-2"
).client("iam")

role_name = "Role-retaildemostore-products-PersonalizeS3"

response = iam.get_role(RoleName=role_name)
role_arn = response["Role"]["Arn"]
print(json.dumps(response["Role"], indent=2, default=str))


# Create Import Jobs

import_job_suffix = str(uuid.uuid4())[:8]

items_create_dataset_import_job_response = personalize.create_dataset_import_job(
    jobName="retaildemostore-products-items-" + import_job_suffix,
    datasetArn=items_dataset_arn,
    dataSource={"dataLocation": "s3://{}/{}".format(bucket, items_filename)},
    roleArn=role_arn,
)

items_dataset_import_job_arn = items_create_dataset_import_job_response[
    "datasetImportJobArn"
]
print(json.dumps(items_create_dataset_import_job_response, indent=2))
