import pytest
import requests
from datetime import datetime
import json
from src.extract import GuardianAPI
from unittest.mock import patch




# test_API_Key_Validation:
def test_guardian_api_retrieves_api_key():
    """Tests: creates instance, stores API key, covers any None/empty keys"""
    
    test_key = "valid-api-key"
    client = GuardianAPI(api_key=test_key)
    assert client.api_key == test_key

    # Rejects Empty
    with pytest.raises(ValueError, match="Valid API key is required"):
        GuardianAPI(api_key="")
    
   
def test_guardian_api_gets_article_data():
    """Tests: that we are pulling Guardian's JSON """


@pytest.mark.skip
def test_search_articles_accepts_search_terms():
    """Tests: search articles method - tests date & search terms"""


# Processing of JSON Data

@pytest.mark.skip
@patch('src.extract.requests')
def test_returns_required_fields(mock_requests):
    """Tests: webPublicationDate, webTitle, webUrl all returned correctly"""


@pytest.mark.skip
def test_returns_publication_date_after_date_selected(mock_requests):
    """Tests: publication date is after date_from value"""
 

@pytest.mark.skip
@patch('src.extract.requests')
def test_returns_content_preview_max_1000_chars(mock_requests):
    """Tests: content preview is limited to 1000 chars"""


@pytest.mark.skip
@patch('src.extract.requests')
def test_returns_last_10_articles_max(mock_requests):
    """Tests: the last 10 articles are provided & 10 articles are the limit """
 

