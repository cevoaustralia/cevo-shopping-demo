import json
import gzip

with gzip.open("data/users.json.gz", mode="rt") as f:
    data = json.loads(f.read())


def handler(event, context):
    print("received event:")
    print(event)

    if event["queryStringParameters"] is not None:
        personaFilter = event["queryStringParameters"]["persona"]
        filteredData = [x for x in data if x["persona"] == personaFilter]
    elif event["pathParameters"] is not None:
        proxySplit = event["pathParameters"]["proxy"].split("/")
        if proxySplit[0] == "persona":
            if len(proxySplit) >= 2:
                # /persona/{persona} return only that persona
                personaFilter = event["pathParameters"]["proxy"].split("/")[1]
                filteredData = [x for x in data if x["persona"] == personaFilter]
            else:
                # /persona only, return all personas types here
                filteredData = {x["persona"]: x for x in data}.values()
                filteredData = [x["persona"] for x in list(filteredData)]
        else:
            return handlerBadRequestError()
    else:
        filteredData = data

    top_n_data = filteredData[:30]

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        },
        "body": json.dumps(top_n_data, indent=4, sort_keys=True, default=str),
    }


def handlerBadRequestError():
    response = "Bad Request Error"
    return {
        "statusCode": 400,
        "headers": {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        },
        "body": json.dumps(response, indent=4, sort_keys=True, default=str),
    }
