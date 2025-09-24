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
        url = f"{self.base_url}?q={query}&api-key={self.api_key}"
        response = requests.get(url)    
        data = response.json()

        #"Creates new dict from JSON response. Provides required fields "webPublicationDate", "webTitle", "webUrl"
        articles = data["response"]["results"][0]

        response_formatted = {
            "webPublicationDate": articles["webPublicationDate"],
            "webTitle": articles["webTitle"],
            "webUrl": articles["webUrl"]
        }
        
        return response_formatted
    