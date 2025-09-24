import requests
import json
from datetime import datetime
import pprint


class GuardianAPI:

    base_url = "https://content.guardianapis.com/search?api-key="


    def __init__(self, api_key):
            if not api_key:
                raise ValueError("Valid API key is required")
            self.api_key = api_key


    def search_articles(self, api_key):

        response = requests.get(self.base_url)    
        data = response.json()
        return data["response"]["results"]