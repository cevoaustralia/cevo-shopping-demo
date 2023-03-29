import boto3
import json
import time
from botocore.exceptions import ClientError
import uuid
import logging

personalize = boto3.Session(
    profile_name=<aws-profile-replace-me>, region_name="ap-southeast-2"
).client("personalize")

logger = logging.getLogger()


def _delete_datasets_and_schemas(dataset_group_arn):
    dataset_arns = []
    schema_arns = []

    dataset_paginator = personalize.get_paginator("list_datasets")
    for dataset_page in dataset_paginator.paginate(datasetGroupArn=dataset_group_arn):
        for dataset in dataset_page["datasets"]:
            describe_response = personalize.describe_dataset(
                datasetArn=dataset["datasetArn"]
            )
            schema_arns.append(describe_response["dataset"]["schemaArn"])

            if dataset["status"] in ["ACTIVE", "CREATE FAILED"]:
                logger.info("Deleting dataset " + dataset["datasetArn"])
                print("Deleting dataset " + dataset["datasetArn"])
                personalize.delete_dataset(datasetArn=dataset["datasetArn"])
            elif dataset["status"].startswith("DELETE"):
                logger.warning(
                    "Dataset {} is already being deleted so will wait for delete to complete".format(
                        dataset["datasetArn"]
                    )
                )
            else:
                raise Exception(
                    "Dataset {} has a status of {} so cannot be deleted".format(
                        dataset["datasetArn"], dataset["status"]
                    )
                )

            dataset_arns.append(dataset["datasetArn"])

    max_time = time.time() + 30 * 60  # 30 mins
    while time.time() < max_time:
        for dataset_arn in dataset_arns:
            try:
                describe_response = personalize.describe_dataset(datasetArn=dataset_arn)
                logger.debug(
                    "Dataset {} status is {}".format(
                        dataset_arn, describe_response["dataset"]["status"]
                    )
                )
            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code == "ResourceNotFoundException":
                    dataset_arns.remove(dataset_arn)

        if len(dataset_arns) == 0:
            logger.info(
                "All datasets have been deleted or none exist for dataset group"
            )
            break
        else:
            logger.info(
                "Waiting for {} dataset(s) to be deleted".format(len(dataset_arns))
            )
            time.sleep(20)

    if len(dataset_arns) > 0:
        raise Exception("Timed out waiting for all datasets to be deleted")

    for schema_arn in schema_arns:
        try:
            logger.info("Deleting schema " + schema_arn)
            personalize.delete_schema(schemaArn=schema_arn)
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "ResourceInUseException":
                logger.info(
                    "Schema {} is still in-use by another dataset (likely in another dataset group)".format(
                        schema_arn
                    )
                )
            else:
                raise e

    logger.info(
        "All schemas used exclusively by datasets have been deleted or none exist for dataset group"
    )

ssm = boto3.Session(
    profile_name=<aws-profile-replace-me>, region_name="ap-southeast-2"
).client("ssm")
recommenderArn = ssm.get_parameter(
    Name="/cevo-shopping-demo/recommender/arn-retaildemostore-recommended-for-you",
    WithDecryption=False,
)

_delete_datasets_and_schemas(recommenderArn["Parameter"]["Value"])
