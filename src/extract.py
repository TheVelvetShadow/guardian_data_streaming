import requests
import json
from datetime import datetime
import pprint


class GuardianAPI:

    def __init__(self, api_key):
            if not api_key:
                raise ValueError("Valid API key is required")
            self.api_key = api_key
            self.base_url = "https://content.guardianapis.com/search"


    def search_articles(self, query=str):

        # Adds API Key & Search Query to base url
        if query:
            url = f"{self.base_url}?q={query}&api-key={self.api_key}"
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
    
    