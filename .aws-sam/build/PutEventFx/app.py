import json
from urllib.error import HTTPError
# This is a sample Python script.
from urllib.request import urlopen

import boto3
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Api

app = Flask(__name__)

api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
BASE_ROUTE = "/weather"
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')


def put_lambda_handler(event, context):
    with app.app_context():
        data = event

        table = dynamodb.Table("DayToDay")
        # if event['method'] == "PUT":
        try:
            response = table.get_item(
                Key={
                    'trip': "Yosemite",
                }
            )

            i = response["Item"][data["day"]]


            newEvent = {
                "order": len(response["Item"][data["day"]]) + 1,
                "event": data["message"]
            }
            response = table.update_item(
                Key={
                    'trip': "Yosemite",
                },
                UpdateExpression='SET #{} = list_append({}, :tempval)'.format(data['day'], data['day']),
                ExpressionAttributeNames={
                    '#{}'.format(data['day']): '{}'.format(data['day'])
                },
                ExpressionAttributeValues={
                    ':tempval': [newEvent]
                },
            )

            print("---------------------------------")
            return json.dumps(response, default=str).strip("'\'")



        except Exception as a:
            print(a)
            return jsonify({"message": str(a)})

    # else:
    #     return jsonify({"Message": "Method doesnt exist"})



