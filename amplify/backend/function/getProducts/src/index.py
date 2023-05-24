import json
import yaml
import boto3
import os
import pandas as pd
import io

# import pickle

# from scipy import sparse
# import pandas as pd
session = boto3.Session(
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    region_name=os.environ["AWS_DEFAULT_REGION"],
)

# set this flag accordingly to use recommender or not
use_recommender = False
use_mf_recommender = True  # matrix factorization
personalizeRuntime = boto3.client("personalize-runtime")

with open("data/products.yaml", "r") as stream:
    data = yaml.safe_load(stream)


def get_s3_to_df(filename):
    session = boto3.Session(
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        region_name=os.environ["AWS_DEFAULT_REGION"],
    )
    s3 = session.resource("s3")
    obj = s3.Object(os.environ["BUCKET_NAME"], f"fake_data/{filename}")
    body = obj.get()["Body"].read()
    df = pd.read_csv(io.BytesIO(body), encoding="utf8")
    return df


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


def get_user_index(user_id):
    return 1


def call_recommend(ml_model, user_items, user_idx, N=20):
    """
    Call the recommend function to get the top N recommendations for a user
    """
    num_recomm = N
    recommendations_raw = ml_model.recommend(
        user_idx, user_items[user_idx], N=num_recomm
    )
    predictions = recommendations_raw[0][
        :num_recomm
    ]  # these are the top n preditictions using the train set
    # index = 0
    # for item in recommendations_raw[0][:num_recomm]:
    #     print(f"item idx: {item}, score: {recommendations_raw[1][index]}")
    #     index += 1

    return predictions


grouped_df = get_s3_to_df("interactions-confidence.csv")
# items_df = pd.read_csv("data/items.csv")
print(f"Grouped df: {grouped_df.head()}")


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
                top_n_data = filteredData[:20]
            elif use_mf_recommender:
                print("Calling matrix factorization recommender...4")
                # sparse_person_content = sparse.csr_matrix(
                #     (
                #         grouped_df["CONFIDENCE"].astype(float),
                #         (grouped_df["USER_IDX"], grouped_df["ITEM_IDX"]),
                #     )
                # )
                # model = pickle.load(
                #     open("data/mf-recommender-2023-05-19-06-01-53.pkl", "rb")
                # )
                # item_indices = call_recommend(model, sparse_person_content, 34, N=20)
                # print(f"item_indices: {item_indices}")
                filteredData = data  # Not using recommender
                top_n_data = filteredData[:20]
            else:
                print("Calling default....")
                filteredData = data  # Not using recommender
                top_n_data = filteredData[:20]
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
            top_n_data = filteredData[:20]
        elif use_mf_recommender:
            print("Calling matrix factorization recommender..3")
            filteredData = data  # Not using recommender
            top_n_data = filteredData[:20]
        else:
            print("Calling default...")
            filteredData = data
            top_n_data = filteredData[:20]

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        },
        "body": json.dumps(top_n_data, indent=4, sort_keys=True, default=str),
    }
