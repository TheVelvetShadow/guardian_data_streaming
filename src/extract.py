import requests
import json
from datetime import datetime
import pprint
import os
import boto3
import logging

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
    
# Logging of API calls
logger = logging.getLogger()
logger.setLevel(logging.INFO)



# Lambda Handler - Gets Guardian articles and publishes to SQS queue
def lambda_handler(event, context):
    try:
        logger.info("Starting Guardian Pipeline")    
        
        # Connects & searches Guardian API
        api_key = os.environ['GUARDIAN_API_KEY']
        api = GuardianAPI(api_key)
        search_term = event.get('search_term', 'Northcoders') 
        articles = api.search_articles(search_term)

        #logs for API Limit in CLoudwatch
        logger.info("Making Guardian API call")  
        
        # Creates SQS client & Message Queue
        sqs = boto3.client('sqs')
        queue_url = os.environ.get('SQS_QUEUE_URL')

        # This sends one SQS message per Article
        for article in articles:
            message_body = json.dumps({
                'webPublicationDate': article['webPublicationDate'],
                'webTitle': article['webTitle'],
                'webUrl': article['webUrl']
            })
            sqs.send_message(QueueUrl=queue_url, MessageBody=message_body)

        
        # Provides read out of succesful function execution
        return {'statusCode': 200, 'body': 'Success'}
    
    except Exception as e:
        # triggers Cloudwatch alarm
        logger.error(f"Pipeline failed: {str(e)}")
        raise
    
    