import requests
import json
from datetime import datetime

class GuardianAPI():
    
    def __init__(self, api_key):
            if not api_key:
                raise ValueError("Valid API key is required")
            self.api_key = api_key

     


