import json
import yaml
import boto3

# set this flag accordingly to use recommender or not
use_recommender = False
personalizeRuntime = boto3.client("personalize-runtime")

with open("data/products.yaml", "r") as stream:
    data = yaml.safe_load(stream)


def get_recommended_items(user_id):
    ssm = boto3.client("ssm")
    recommenderArn = ssm.get_parameter(
        Name="/cevo-shopping-demo/recommender/arn-retaildemostore-recommended-for-you",
        WithDecryption=False,
    )
    response = personalizeRuntime.get_recommendations(
        recommenderArn=recommenderArn["Parameter"]["Value"],
        userId=user_id,
        numResults=30,
    )
    rec_items = [item["itemId"] for item in response["itemList"]]
    print(f"Recommended items: {rec_items}")
    return rec_items


def get_popular_items(user_id="x"):
    ssm = boto3.client("ssm")
    recommenderArn = ssm.get_parameter(
        Name="/cevo-shopping-demo/recommender/arn-retaildemostore-popular-items",
        WithDecryption=False,
    )
    response = personalizeRuntime.get_recommendations(
        recommenderArn=recommenderArn["Parameter"]["Value"],
        userId=user_id,
        numResults=100,
    )
    rec_items = [item["itemId"] for item in response["itemList"]]
    print(f"Popular items: {rec_items}")
    return rec_items


def handler(event, context):
    print("received event:")
    print(event)

    # iterate data and update image property
    basedir = "https://cevo-shopping-demo.s3.ap-southeast-2.amazonaws.com/dataset/images/images"
    top_n_data = []
    for product in data:
        product["installments"] = 4
        product["image"] = (
            product["image"]
            if "http" in product["image"]
            else f"{basedir}/{product['category']}/{product['image']}"
        )

    if event["queryStringParameters"] is not None:
        if event["queryStringParameters"]["user_id"]:
            if use_recommender:
                print("Calling 'recommended for you' recommender...")
                recommended_items = get_recommended_items(
                    event["queryStringParameters"]["user_id"]
                )
                filteredData = [
                    item for item in data if item["id"] in recommended_items
                ]
                filteredData.sort(key=lambda x: recommended_items.index(x["id"]))
                top_n_data = filteredData
            else:
                filteredData = data  # Not using recommender
                top_n_data = filteredData
        else:
            categoryFilter = event["queryStringParameters"]["filters"]
            filteredData = [x for x in data if x["category"] == categoryFilter]
            print(
                f"Type of categoryFilter: {type(categoryFilter)}, contents: {categoryFilter}."
            )
            top_n_data = filteredData[:30]
    else:
        if use_recommender:
            print("Calling 'popular items' recommender...")
            popular_items = get_popular_items()
            filteredData = [item for item in data if item["id"] in popular_items]
            filteredData.sort(key=lambda x: popular_items.index(x["id"]))
            top_n_data = filteredData
        else:
            filteredData = data
            top_n_data = filteredData

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        },
        "body": json.dumps(top_n_data, indent=4, sort_keys=True, default=str),
    }
