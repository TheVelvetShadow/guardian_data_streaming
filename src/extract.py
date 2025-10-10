import requests
import json
import os
import boto3
import logging


class GuardianAPI:

    def __init__(self, api_key):
        if not api_key:
            raise ValueError("Valid API key is required")
        self.api_key = api_key
        # Most recent results are returned first. page-size limits to 10 articles as per brief
        self.base_url = "https://content.guardianapis.com/search?"
        

# https://content.guardianapis.com/search?section=content&from-date=2025-10-10&page-size=10&q=trump&api-key=test


    def search_articles(self, query=None, date_from=None):
        
        # Builds APIAmend values here if you wish to
        order_by = "order-by=newest"
        page_size = "page-size=10"
        
        url = self.base_url
        if date_from: 
                url += f"from-date={date_from}&"
        url += f"{order_by}&{page_size}"
        if query:   
            url += f"&q={query}"           
        url += f"&api-key={self.api_key}"

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

        # logs for API Limit in CLoudwatch
        logger.info("Making Guardian API call")

        # Creates SQS client & Message Queue
        sqs = boto3.client('sqs')
        queue_url = os.environ.get('SQS_QUEUE_URL')

        # This sends one SQS message per Article result
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
        # 'failed' triggers Cloudwatch alarm
        logger.error(f"Pipeline failed: {str(e)}")
        raise
