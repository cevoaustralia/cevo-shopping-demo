import boto3
import json
import time
from botocore.exceptions import ClientError

personalize = boto3.Session(
    profile_name=<aws-profile-replace-me>, region_name="ap-southeast-2"
).client("personalize")

# First, let's list the recipes in the ecommerce domain
response = personalize.list_recipes(domain="ECOMMERCE")
print(json.dumps(response["recipes"], indent=2, default=str))


ssm = boto3.Session(
    profile_name=<aws-profile-replace-me>, region_name="ap-southeast-2"
).client("ssm")
datasetGroupArn = ssm.get_parameter(
    Name="/cevo-shopping-demo/dataset-group/arn-retaildemostore",
    WithDecryption=False,
)
DATASET_GROUP_ARN = datasetGroupArn["Parameter"]["Value"]


def create_recommended_for_you_recommender():
    try:
        response = personalize.create_recommender(
            name="retaildemostore-recommended-for-you",
            recipeArn="arn:aws:personalize:::recipe/aws-ecomm-recommended-for-you",
            datasetGroupArn=DATASET_GROUP_ARN,
        )
        rfy_recommender_arn = response["recommenderArn"]
        print(f"Recommended For You recommender ARN = {rfy_recommender_arn}")
        return rfy_recommender_arn
    except personalize.exceptions.ResourceAlreadyExistsException:
        print("You aready created this recommender, seemingly")
        paginator = personalize.get_paginator("list_recommenders")
        for paginate_result in paginator.paginate(datasetGroupArn=DATASET_GROUP_ARN):
            for recommender in paginate_result["recommenders"]:
                if recommender["name"] == "retaildemostore-recommended-for-you":
                    rfy_recommender_arn = recommender["recommenderArn"]
                    break


def create_popular_items_by_views_recommender():
    try:
        response = personalize.create_recommender(
            name="retaildemostore-popular-items",
            recipeArn="arn:aws:personalize:::recipe/aws-ecomm-popular-items-by-views",
            datasetGroupArn=DATASET_GROUP_ARN,
        )
        most_viewed_recommender_arn = response["recommenderArn"]
        print(f"Most Viewed recommender ARN = {most_viewed_recommender_arn}")
        return most_viewed_recommender_arn
    except personalize.exceptions.ResourceAlreadyExistsException:
        print("You aready created this recommender, seemingly")
        paginator = personalize.get_paginator("list_recommenders")
        for paginate_result in paginator.paginate(datasetGroupArn=DATASET_GROUP_ARN):
            for recommender in paginate_result["recommenders"]:
                if recommender["name"] == "retaildemostore-popular-items":
                    most_viewed_recommender_arn = recommender["recommenderArn"]
                    break


def wait_for_recommenders_solution_version_creation(
    rfy_recommender_arn, most_viewed_recommender_arn
):
    recommender_arns = [rfy_recommender_arn, most_viewed_recommender_arn]

    max_time = time.time() + 3 * 60 * 60  # 3 hours
    while time.time() < max_time:
        for recommender_arn in reversed(recommender_arns):
            response = personalize.describe_recommender(recommenderArn=recommender_arn)
            status = response["recommender"]["status"]

            if status == "ACTIVE":
                print(f"Recommender {recommender_arn} successfully completed")
                recommender_arns.remove(recommender_arn)
            elif status == "CREATE FAILED":
                print(f"Recommender {recommender_arn} failed")
                if response["recommender"].get("failureReason"):
                    print("   Reason: " + response["recommender"]["failureReason"])
                recommender_arns.remove(recommender_arn)

        if len(recommender_arns) > 0:
            print("At least one recommender is still in progress")
            time.sleep(60)
        else:
            print("All recommenders have completed")
            break


# When we create recommenders, this is when the training happens, and this is done on the
# datasets that we have submitted to the dataset group. Training takes a while, like for our case,
# this will likely take about an hour to complete
rfy_recommender_arn = create_recommended_for_you_recommender()
most_viewed_recommender_arn = create_popular_items_by_views_recommender()
wait_for_recommenders_solution_version_creation(
    rfy_recommender_arn, most_viewed_recommender_arn
)
