import boto3

personalizeRt = boto3.Session(
    profile_name=<aws-profile-replace-me>, region_name="ap-southeast-2"
).client("personalize-runtime")
ssm = boto3.Session(
    profile_name=<aws-profile-replace-me>, region_name="ap-southeast-2"
).client("ssm")
recommenderArn = ssm.get_parameter(
    Name="/cevo-shopping-demo/recommender/arn-retaildemostore-recommended-for-you",
    WithDecryption=False,
)


response = personalizeRt.get_recommendations(
    recommenderArn=recommenderArn["Parameter"]["Value"],
    userId="1870",
    numResults=20,
)

print("Recommended items")
for item in response["itemList"]:
    print(item)
