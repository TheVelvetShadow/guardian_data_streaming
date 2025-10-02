import requests
import json
from datetime import datetime
import pprint
import os
import boto3

class GuardianAPI:

    def __init__(self, api_key):
            if not api_key:
                raise ValueError("Valid API key is required")
            self.api_key = api_key
            # page-size limits to 10 articles as per brief
            self.base_url = "https://content.guardianapis.com/search?order-by=newest&page-size=10"


    def search_articles(self, query=str):

        # Adds API Key & Search Query to base url
        if query:
            url = f"{self.base_url}&q={query}&api-key={self.api_key}"
        else:
            url = f"{self.base_url}?api-key={self.api_key}"

        # Requests JSON response from API and presents in list of dictionaries
        response = requests.get(url)    
        data = response.json()
        results = data["response"]["results"]

        # Formats JSON data
        # Creates new dict from JSON response. 
        # Provides required fields "webPublicationDate", "webTitle", "webUrl"
        formatted_articles = []

        for article in results:
            formatted_articles.append({
            "webPublicationDate": article["webPublicationDate"],
            "webTitle": article["webTitle"],
            "webUrl": article["webUrl"]
        })
       
        return formatted_articles
    




# Lambda Handler - Gets Guardian articles and publishes to SQS queue
def lambda_handler(event, context):
    # Gets API Key
    api_key = os.environ['GUARDIAN_API_KEY']
    
    # Calls Guardian API Class & Applies API Key
    api = GuardianAPI(api_key)
    
    # Gets Search term, provides Northcoders as default
    search_term = event.get('search_term', 'Northcoders') 

    # Applies Search term 
    articles = api.search_articles(search_term)

    # Creates SQS client
    sqs = boto3.client('sqs')

    # Send search result to SQS
    # send_message needs Queue url to send message to
    # create SQS Queue
    queue_url = os.environ.get('SQS_QUEUE_URL')

    # Define message to be sent to SQS (article data as JSON string)
    # This sends one SQS message per Article
    for article in articles:
        message_body = json.dumps({
            'webPublicationDate': article['webPublicationDate'],
            'webTitle': article['webTitle'],
            'webUrl': article['webUrl']
        })
        # send message to Q
        sqs.send_message(QueueUrl=queue_url, MessageBody=message_body)

    # Provides read out of succesful function execution
    return {'statusCode': 200, 'body': 'Success'}
   
    
    