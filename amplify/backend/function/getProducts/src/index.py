import json
import pandas as pd


def handler(event, context):
    print("received event:")
    print(event)

    df = pd.DataFrame(
        [
            ["Ajitesh", 84, 183, "no"],
            ["Shailesh", 79, 186, "yes"],
            ["Seema", 67, 158, "yes"],
            ["Nidhi", 52, 155, "no"],
        ]
    )

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        },
        "body": json.dumps(df.values.tolist(), indent=4, sort_keys=True, default=str),
    }
