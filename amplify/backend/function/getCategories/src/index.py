import json
import yaml
import random

# "categories.yaml" is a file in the same directory as this file
with open("data/categories.yaml", "r") as stream:
    data = yaml.safe_load(stream)


def handler(event, context):
    print("received event:")
    print(event)

    # iterate data and update image property
    basedir = "https://cevo-shopping-demo.s3.ap-southeast-2.amazonaws.com/dataset/images/images"
    for product in data:
        product["image"] = (
            product["image"]
            if "http" in product["image"]
            else f"{basedir}/{product['name']}/{product['image']}"
        )

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        },
        "body": json.dumps(data, indent=4, sort_keys=True, default=str),
    }
