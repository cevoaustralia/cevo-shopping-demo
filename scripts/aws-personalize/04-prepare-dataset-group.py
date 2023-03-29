import boto3
import json
import time
from botocore.exceptions import ClientError
import uuid

personalize = boto3.Session(
    profile_name=<aws-profile-replace-me>, region_name="ap-southeast-2"
).client("personalize")


def delete_schema(schema_name):
    schemas = personalize.list_schemas()
    schema = next((x for x in schemas["schemas"] if x["name"] == schema_name), None)
    try:
        if schema is None:
            print(f"Schema {schema_name} does not exist")
            return
        print(f"Deleting schema for {schema_name}...")
        personalize.delete_schema(schemaArn=schema["schemaArn"])
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "ResourceNotFoundException":
            print("Schema {} does not exist".format(schema))
        else:
            raise e


def create_items_schema():
    print("Creating Items Schema")
    items_schema = {
        "type": "record",
        "name": "Items",
        "namespace": "com.amazonaws.personalize.schema",
        "fields": [
            {"name": "ITEM_ID", "type": "string"},
            {"name": "PRICE", "type": "float"},
            {
                "name": "CATEGORY_L1",
                "type": "string",
                "categorical": True,
            },
            {
                "name": "CATEGORY_L2",
                "type": "string",
                "categorical": True,
            },
            {"name": "PRODUCT_DESCRIPTION", "type": "string", "textual": True},
            {
                "name": "GENDER",
                "type": "string",
                "categorical": True,
            },
            {"name": "PROMOTED", "type": "string"},
        ],
        "version": "1.0",
    }

    try:
        create_schema_response = personalize.create_schema(
            name="retaildemostore-products-items",
            domain="ECOMMERCE",
            schema=json.dumps(items_schema),
        )
        items_schema_arn = create_schema_response["schemaArn"]
        return items_schema_arn
        # print(json.dumps(create_schema_response, indent=2))
    except personalize.exceptions.ResourceAlreadyExistsException:
        print("You aready created this schema, seemingly")
        paginator = personalize.get_paginator("list_schemas")
        for paginate_result in paginator.paginate():
            for schema in paginate_result["schemas"]:
                if schema["name"] == "retaildemostore-products-items":
                    items_schema_arn = schema["schemaArn"]
                    print(f"Using existing schema: {items_schema_arn}")
                    break


def create_user_schema():
    print("Creating Users Schema")
    users_schema = {
        "type": "record",
        "name": "Users",
        "namespace": "com.amazonaws.personalize.schema",
        "fields": [
            {"name": "USER_ID", "type": "string"},
            {"name": "AGE", "type": "int"},
            {
                "name": "GENDER",
                "type": "string",
                "categorical": True,
            },
        ],
        "version": "1.0",
    }

    try:
        create_schema_response = personalize.create_schema(
            name="retaildemostore-products-users",
            domain="ECOMMERCE",
            schema=json.dumps(users_schema),
        )
        # print(json.dumps(create_schema_response, indent=2))
        users_schema_arn = create_schema_response["schemaArn"]
        return users_schema_arn
    except personalize.exceptions.ResourceAlreadyExistsException:
        print("You aready created this schema, seemingly")
        paginator = personalize.get_paginator("list_schemas")
        for paginate_result in paginator.paginate():
            for schema in paginate_result["schemas"]:
                if schema["name"] == "retaildemostore-products-users":
                    users_schema_arn = schema["schemaArn"]
                    print(f"Using existing schema: {users_schema_arn}")
                    break


def create_interactions_schema():
    print("Creating Interactions Schema")
    interactions_schema = {
        "type": "record",
        "name": "Interactions",
        "namespace": "com.amazonaws.personalize.schema",
        "fields": [
            {"name": "ITEM_ID", "type": "string"},
            {"name": "USER_ID", "type": "string"},
            {"name": "EVENT_TYPE", "type": "string"},  # "View", "Purchase", etc.
            {"name": "TIMESTAMP", "type": "long"},
        ],
        "version": "1.0",
    }

    try:
        create_schema_response = personalize.create_schema(
            name="retaildemostore-products-interactions",
            domain="ECOMMERCE",
            schema=json.dumps(interactions_schema),
        )
        # print(json.dumps(create_schema_response, indent=2))
        interactions_schema_arn = create_schema_response["schemaArn"]
        return interactions_schema_arn
    except personalize.exceptions.ResourceAlreadyExistsException:
        print("You aready created this schema, seemingly")
        paginator = personalize.get_paginator("list_schemas")
        for paginate_result in paginator.paginate():
            for schema in paginate_result["schemas"]:
                if schema["name"] == "retaildemostore-products-interactions":
                    interactions_schema_arn = schema["schemaArn"]
                    print(f"Using existing schema: {interactions_schema_arn}")
                    break


def create_dataset_group():
    print("Create Dataset Group")
    try:
        create_dataset_group_response = personalize.create_dataset_group(
            name="retaildemostore-products", domain="ECOMMERCE"
        )
        dataset_group_arn = create_dataset_group_response["datasetGroupArn"]
        # print(json.dumps(create_dataset_group_response, indent=2))
    except personalize.exceptions.ResourceAlreadyExistsException:
        print("You aready created this dataset group, seemingly")
        paginator = personalize.get_paginator("list_dataset_groups")
        for paginate_result in paginator.paginate():
            for dataset_group in paginate_result["datasetGroups"]:
                if dataset_group["name"] == "retaildemostore-products":
                    dataset_group_arn = dataset_group["datasetGroupArn"]
                    break

    print(f"DatasetGroupArn = {dataset_group_arn}")

    print(" Wait for Dataset Group to be ACTIVE")
    status = None
    max_time = time.time() + 3 * 60 * 60  # 3 hours
    while time.time() < max_time:
        describe_dataset_group_response = personalize.describe_dataset_group(
            datasetGroupArn=dataset_group_arn
        )
        status = describe_dataset_group_response["datasetGroup"]["status"]
        print("DatasetGroup: {}".format(status))

        if status == "ACTIVE" or status == "CREATE FAILED":
            break

        time.sleep(15)
    return dataset_group_arn


def create_items_dataset(dataset_group_arn, items_schema_arn):
    print("Create Items Dataset")
    try:
        dataset_type = "ITEMS"
        create_dataset_response = personalize.create_dataset(
            name="retaildemostore-products-items",
            datasetType=dataset_type,
            datasetGroupArn=dataset_group_arn,
            schemaArn=items_schema_arn,
        )

        items_dataset_arn = create_dataset_response["datasetArn"]
        print(f"Items dataset ARN = {items_dataset_arn}")
        return items_dataset_arn
        # print(json.dumps(create_dataset_response, indent=2))
    except personalize.exceptions.ResourceAlreadyExistsException:
        print("You aready created this dataset, seemingly")
        paginator = personalize.get_paginator("list_datasets")
        for paginate_result in paginator.paginate(datasetGroupArn=dataset_group_arn):
            for dataset in paginate_result["datasets"]:
                if dataset["name"] == "retaildemostore-products-items":
                    items_dataset_arn = dataset["datasetArn"]
                    break


def create_users_dataset(dataset_group_arn, users_schema_arn):
    print("Create Users Dataset")
    try:
        dataset_type = "USERS"
        create_dataset_response = personalize.create_dataset(
            name="retaildemostore-products-users",
            datasetType=dataset_type,
            datasetGroupArn=dataset_group_arn,
            schemaArn=users_schema_arn,
        )

        users_dataset_arn = create_dataset_response["datasetArn"]
        print(f"Users dataset ARN = {users_dataset_arn}")
        return users_dataset_arn
        # print(json.dumps(create_dataset_response, indent=2))
    except personalize.exceptions.ResourceAlreadyExistsException:
        print("You aready created this dataset, seemingly")
        paginator = personalize.get_paginator("list_datasets")
        for paginate_result in paginator.paginate(datasetGroupArn=dataset_group_arn):
            for dataset in paginate_result["datasets"]:
                if dataset["name"] == "retaildemostore-products-users":
                    users_dataset_arn = dataset["datasetArn"]
                    break


def create_interactions_dataset(dataset_group_arn, interactions_schema_arn):
    print("Create Interactions Dataset")
    try:
        dataset_type = "INTERACTIONS"
        create_dataset_response = personalize.create_dataset(
            name="retaildemostore-products-interactions",
            datasetType=dataset_type,
            datasetGroupArn=dataset_group_arn,
            schemaArn=interactions_schema_arn,
        )

        interactions_dataset_arn = create_dataset_response["datasetArn"]
        print(f"Interactions dataset ARN = {interactions_dataset_arn}")
        return interactions_dataset_arn
        # print(json.dumps(create_dataset_response, indent=2))
    except personalize.exceptions.ResourceAlreadyExistsException:
        print("You aready created this dataset, seemingly")
        paginator = personalize.get_paginator("list_datasets")
        for paginate_result in paginator.paginate(datasetGroupArn=dataset_group_arn):
            for dataset in paginate_result["datasets"]:
                if dataset["name"] == "retaildemostore-products-interactions":
                    interactions_dataset_arn = dataset["datasetArn"]
                    break


def wait_for_datasets_to_be_active(
    items_dataset_arn, users_dataset_arn, interactions_dataset_arn
):
    print("Wait for Datasets to be ACTIVE")
    dataset_arns = [items_dataset_arn, users_dataset_arn, interactions_dataset_arn]

    max_time = time.time() + 3 * 60 * 60  # 3 hours
    while time.time() < max_time:
        for dataset_arn in reversed(dataset_arns):
            response = personalize.describe_dataset(datasetArn=dataset_arn)
            status = response["dataset"]["status"]

            if status == "ACTIVE":
                print(f"Dataset {dataset_arn} successfully completed")
                dataset_arns.remove(dataset_arn)
            elif status == "CREATE FAILED":
                print(f"Dataset {dataset_arn} failed")
                if response["dataset"].get("failureReason"):
                    print("   Reason: " + response["dataset"]["failureReason"])
                dataset_arns.remove(dataset_arn)

        if len(dataset_arns) > 0:
            print("At least one dataset is still in progress")
            time.sleep(15)
        else:
            print("All datasets have completed")
            break


def import_datasets_to_personalize(
    items_dataset_arn, users_dataset_arn, interactions_dataset_arn
):
    print("Import Datasets to Personalize")
    bucket = "cevo-shopping-demo"
    users_filename = "users.csv"
    items_filename = "items.csv"
    interactions_filename = "interactions.csv"

    s3 = boto3.Session(
        profile_name=<aws-profile-replace-me>, region_name="ap-southeast-2"
    ).client("s3")

    response = s3.get_bucket_policy(Bucket=bucket)
    # print(json.dumps(json.loads(response["Policy"]), indent=2))

    iam = boto3.Session(
        profile_name=<aws-profile-replace-me>, region_name="ap-southeast-2"
    ).client("iam")

    role_name = "Role-retaildemostore-products-PersonalizeS3"

    response = iam.get_role(RoleName=role_name)
    role_arn = response["Role"]["Arn"]
    # print(json.dumps(response["Role"], indent=2, default=str))

    print("Items Dataset Import Job")
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
    # print(json.dumps(items_create_dataset_import_job_response, indent=2))

    print("Users Dataset Import Job")
    users_create_dataset_import_job_response = personalize.create_dataset_import_job(
        jobName="retaildemostore-products-users-" + import_job_suffix,
        datasetArn=users_dataset_arn,
        dataSource={"dataLocation": "s3://{}/{}".format(bucket, users_filename)},
        roleArn=role_arn,
    )

    users_dataset_import_job_arn = users_create_dataset_import_job_response[
        "datasetImportJobArn"
    ]
    # print(json.dumps(users_create_dataset_import_job_response, indent=2))

    print("Interactions Dataset Import Job")
    interactions_create_dataset_import_job_response = (
        personalize.create_dataset_import_job(
            jobName="retaildemostore-products-interactions-" + import_job_suffix,
            datasetArn=interactions_dataset_arn,
            dataSource={
                "dataLocation": "s3://{}/{}".format(bucket, interactions_filename)
            },
            roleArn=role_arn,
        )
    )

    interactions_dataset_import_job_arn = (
        interactions_create_dataset_import_job_response["datasetImportJobArn"]
    )
    # print(json.dumps(interactions_create_dataset_import_job_response, indent=2))

    print("Wait for Import Jobs to complete")

    import_job_arns = [
        items_dataset_import_job_arn,
        users_dataset_import_job_arn,
        interactions_dataset_import_job_arn,
    ]

    max_time = time.time() + 3 * 60 * 60  # 3 hours
    while time.time() < max_time:
        for job_arn in reversed(import_job_arns):
            import_job_response = personalize.describe_dataset_import_job(
                datasetImportJobArn=job_arn
            )
            status = import_job_response["datasetImportJob"]["status"]

            if status == "ACTIVE":
                print(f"Import job {job_arn} successfully completed")
                import_job_arns.remove(job_arn)
            elif status == "CREATE FAILED":
                print(f"Import job {job_arn} failed")
                if import_job_response["datasetImportJob"].get("failureReason"):
                    print(
                        "   Reason: "
                        + import_job_response["datasetImportJob"]["failureReason"]
                    )
                import_job_arns.remove(job_arn)

        if len(import_job_arns) > 0:
            print("At least one dataset import job still in progress")
            time.sleep(60)
        else:
            print("All import jobs have ended")
            break


print("Start by clearing out existing schemas... ")
delete_schema("retaildemostore-products-items")
delete_schema("retaildemostore-products-users")
delete_schema("retaildemostore-products-interactions")
delete_schema("retaildemostore-products-interactions-v2")
items_schema_arn = create_items_schema()
users_schema_arn = create_user_schema()
interactions_schema_arn = create_interactions_schema()
dataset_group_arn = create_dataset_group()
items_dataset_arn = create_items_dataset(dataset_group_arn, items_schema_arn)
users_dataset_arn = create_users_dataset(dataset_group_arn, users_schema_arn)
interactions_dataset_arn = create_interactions_dataset(
    dataset_group_arn, interactions_schema_arn
)
wait_for_datasets_to_be_active(
    items_dataset_arn, users_dataset_arn, interactions_dataset_arn
)
import_datasets_to_personalize(
    items_dataset_arn, users_dataset_arn, interactions_dataset_arn
)
