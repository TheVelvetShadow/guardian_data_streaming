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

    def search_articles(self, query=None, date_from=None):

        # Vars for building API request, adds vars to base URL -- amend values here if you wish to
        order_by = "order-by=newest"
        # returns only articles
        articles = "type=article"
        # returns 10 articles
        page_size = "page-size=10"

        url = self.base_url
        # Checks if date from value is provided
        if date_from:
            url += f"from-date={date_from}&"

        url += f"{order_by}&{articles}&{page_size}"

        if query:
            url += f"&q={query}"
        # Note - I found using the APIs "show-blocks" preferable over
        # "show-fields" for parsing the text body
        url += "&show-blocks=body"
        url += f"&api-key={self.api_key}"

        # Requests JSON response from API and presents in list of dictionaries
        response = requests.get(url, timeout=30)
        # Formats JSON data
        data = response.json()
        # Creates new dict from JSON response.
        results = data["response"]["results"]

        # var Provides required fields "webPublicationDate", "webTitle", "webUrl & "Content Preview"
        formatted_articles = []

        for article in results:
            # iterate the results arr - list of dicts
            # access the blocks key - value is dict
            # access the body in blocks dict
            # the blocks value is a list of dicts
            # access the bodyTextSummary key
            # used .get to avoid keyerrors

            blocks = article.get("blocks", {})
            # access the body in blocks dict  - the body value is a list of dicts
            body_blocks = blocks.get("body", [])

            content_preview = ""
            if body_blocks and len(body_blocks) > 0:
                content_preview = body_blocks[0].get("bodyTextSummary", "")[
                    :1000]  # access the bodyTextSummary key

            formatted_articles.append({
                "webPublicationDate": article["webPublicationDate"],
                "webTitle": article["webTitle"],
                "webUrl": article["webUrl"],
                "contentPreview": content_preview
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
                'webUrl': article['webUrl'],
                'contentPreview': article['contentPreview']
            })
            sqs.send_message(QueueUrl=queue_url, MessageBody=message_body)

        # Provides read out of succesful function execution
        return {'statusCode': 200,
                'body': json.dumps({'message': 'Success',
                                    'articles_processed': len(articles)
                                    })
                }

    except Exception as e:
        # 'failed' triggers Cloudwatch alarm
        logger.error(f"Pipeline failed: {str(e)}")
        raise
