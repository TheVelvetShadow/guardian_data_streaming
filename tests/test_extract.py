import pytest
import requests
from datetime import datetime
import json
from src.extract import GuardianAPI, lambda_handler
from unittest.mock import patch, Mock
import os

# ===== fixtures & variables =====
# Fixtures of Guardian API responses used for mocking. Return raw response.
@pytest.fixture
def mock_guardian_api_one_response(): 
        return {
            "response": {
            "status": "ok",
            "userTier": "developer",
            "total": 2614948,
            "startIndex": 1,
            "pageSize": 10,
            "currentPage": 1,
            "pages": 261495,
            "orderBy": "newest",
            "results": [
            {
                "id": "sport/live/2025/sep/24/nottinghamshire-v-warwickshire-hampshire-v-surrey-and-more-county-cricket-live",
                "type": "liveblog",
                "sectionId": "sport",
                "sectionName": "Sport",
                "webPublicationDate": "2025-09-24T11:19:26Z",
                "webTitle": "Nottinghamshire v Warwickshire, tributes paid to Dickie Bird, and more: county cricket – live",
                "webUrl": "https://www.theguardian.com/sport/live/2025/sep/24/nottinghamshire-v-warwickshire-hampshire-v-surrey-and-more-county-cricket-live",
                "apiUrl": "https://content.guardianapis.com/sport/live/2025/sep/24/nottinghamshire-v-warwickshire-hampshire-v-surrey-and-more-county-cricket-live",
                "isHosted": False,
                "pillarId": "pillar/sport",
                "pillarName": "Sport"
            },
            ]
        }
        }

@pytest.fixture
def mock_guardian_api_multiple_responses():    
        # simulates API query of keyword 'trump"
        return {
            "response": {
                "status": "ok",
                "userTier": "developer",
                "total": 2614948,
                "startIndex": 1,
                "pageSize": 10,
                "currentPage": 1,
                "pages": 261495,
                "orderBy": "newest",
                "results": [
                {
                    "id": "us-news/live/2025/sep/24/donald-trump-jimmy-kimmel-freedom-of-speech-immigration-government-shutdown-us-politics-live-news-updates",
                    "type": "liveblog",
                    "sectionId": "us-news",
                    "sectionName": "US news",
                    "webPublicationDate": "2025-09-24T11:15:59Z",
                    "webTitle": "Trump says he ‘can’t believe’ Kimmel back on ABC as he hints at action against network – US politics live",
                    "webUrl": "https://www.theguardian.com/us-news/live/2025/sep/24/donald-trump-jimmy-kimmel-freedom-of-speech-immigration-government-shutdown-us-politics-live-news-updates",
                    "apiUrl": "https://content.guardianapis.com/us-news/live/2025/sep/24/donald-trump-jimmy-kimmel-freedom-of-speech-immigration-government-shutdown-us-politics-live-news-updates",
                    "isHosted": False,
                    "pillarId": "pillar/news",
                    "pillarName": "News"
                },
                {
                    "id": "world/live/2025/sep/24/russia-ukraine-trump-zelenskyy-unga-drones-europe-latest-news-updates",
                    "type": "liveblog",
                    "sectionId": "world",
                    "sectionName": "World news",
                    "webPublicationDate": "2025-09-24T11:02:21Z",
                    "webTitle": "‘No alternative’ to continuing invasion, claims Russia, as Trump says Ukraine could regain all land lost – latest updates",
                    "webUrl": "https://www.theguardian.com/world/live/2025/sep/24/russia-ukraine-trump-zelenskyy-unga-drones-europe-latest-news-updates",
                    "apiUrl": "https://content.guardianapis.com/world/live/2025/sep/24/russia-ukraine-trump-zelenskyy-unga-drones-europe-latest-news-updates",
                    "isHosted": False,
                    "pillarId": "pillar/news",
                    "pillarName": "News"
                },
                {
                    "id": "sport/2025/sep/24/trump-ryder-cup-spicy-support-use-europe-golf",
                    "type": "article",
                    "sectionId": "sport",
                    "sectionName": "Sport",
                    "webPublicationDate": "2025-09-24T11:01:04Z",
                    "webTitle": "Trump looms large at Ryder Cup where home rules and spicy support are always on show",
                    "webUrl": "https://www.theguardian.com/sport/2025/sep/24/trump-ryder-cup-spicy-support-use-europe-golf",
                    "apiUrl": "https://content.guardianapis.com/sport/2025/sep/24/trump-ryder-cup-spicy-support-use-europe-golf",
                    "isHosted": False,
                    "pillarId": "pillar/sport",
                    "pillarName": "Sport"
                },
                {
                    "id": "us-news/2025/sep/24/trump-tylenol-pregnancy-autism-backlash",
                    "type": "article",
                    "sectionId": "us-news",
                    "sectionName": "US news",
                    "webPublicationDate": "2025-09-24T11:00:07Z",
                    "webTitle": "Trump’s Tylenol announcement incurs furious backlash: ‘This is yet more utter rubbish’",
                    "webUrl": "https://www.theguardian.com/us-news/2025/sep/24/trump-tylenol-pregnancy-autism-backlash",
                    "apiUrl": "https://content.guardianapis.com/us-news/2025/sep/24/trump-tylenol-pregnancy-autism-backlash",
                    "isHosted": False,
                    "pillarId": "pillar/news",
                    "pillarName": "News"
                }
                ]
            }
            } 

# API test key variable
test_key = "test"


##### Guardian API Tests #####


# ===== API Validation =====
# Test 1 - test_API_Key_Validation:
def test_guardian_api_class_accepts_api_key():
    """Tests: accepts API key, covers any None/empty keys"""
    
    client = GuardianAPI(test_key)

    assert client.api_key == test_key
    # Rejects Empty
    with pytest.raises(ValueError, match="Valid API key is required"):
        GuardianAPI(api_key="")


# ===== Search Functionality =====
# Test 2  - tests request is ordered by newest articles
@patch('src.extract.requests.get')
def test_returns_latest_articles_max(mock_get):
    
    client = GuardianAPI("test")
    client.search_articles("Warickshire")

    called_url = mock_get.call_args[0][0]

    assert "?order-by=newest" in called_url


# Test 3 - tests request is limited to 10 articles 
@patch('src.extract.requests.get')
def test_returns_10_articles_max(mock_get):
    
    client = GuardianAPI("test")
    client.search_articles("Warickshire")

    called_url = mock_get.call_args[0][0]

    assert "&page-size=10" in called_url


# Test 4 - search query is added to url with api key
@patch("src.extract.requests.get")
def test_search_query_added_to_url(mock_get):

    client = GuardianAPI("test")
    client.search_articles("Warickshire")

    called_url = mock_get.call_args[0][0]

    assert "&q=Warickshire" in called_url


# Test 5 - api key is added to url
@patch("src.extract.requests.get")
def test_api_key_added_to_url(mock_get):

    client = GuardianAPI("test")
    client.search_articles("Warickshire")
    called_url = mock_get.call_args[0][0]

    # Check URL has API + &
    assert "&api-key=test" in called_url


# Test 5 - api key is added to url with no query
@patch("src.extract.requests.get")
def test_api_key_added_to_url_with_no_query(mock_get):

    client = GuardianAPI("test")
    # No search query added
    client.search_articles("")
    called_url = mock_get.call_args[0][0]

    # Check URL has ?
    assert "?api-key=test" in called_url

# Additional Features:

@pytest.mark.skip
def test_returns_publication_date_after_date_selected(mock_requests):
    """Tests: publication date is after date_from value"""


@pytest.mark.skip
@patch('src.extract.requests')
def test_returns_content_preview_max_1000_chars(mock_requests):
    """Tests: content preview is limited to 1000 chars"""


# ===== Processing of JSON Data =====
# Processses JSON to required fields.

# Test 6 - Requested fields; webPublicationDate, webTitle, webUrl all returned correctly
@patch('src.extract.requests.get')
def test_returns_one_formatted_response(mock_requests, mock_guardian_api_one_response):

    # Creates instance of a mock response for requests to access
    mock_response = Mock()
    # creates guardian_api_one as the JSON response
    mock_response.json.return_value = mock_guardian_api_one_response
    # Configures mock_requests to return mocked JSON response
    mock_requests.return_value = mock_response

    client = GuardianAPI(test_key)

    articles = client.search_articles("Warwickshire")
    
    expected_article = [{
            "webPublicationDate": "2025-09-24T11:19:26Z",
            "webTitle": "Nottinghamshire v Warwickshire, tributes paid to Dickie Bird, and more: county cricket – live",
            "webUrl": "https://www.theguardian.com/sport/live/2025/sep/24/nottinghamshire-v-warwickshire-hampshire-v-surrey-and-more-county-cricket-live"
        }
    ]
    assert articles == expected_article


@pytest.mark.skip
# Test 7 - tests formatting for multiple articles
@patch('src.extract.requests.get')
def test_returns_required_fields_multiple_results(mock_requests, mock_guardian_api_multiple_responses):

        mock_response = Mock()
        mock_response.json.return_value =  mock_guardian_api_multiple_responses
        mock_requests.return_value = mock_response

        client = GuardianAPI(test_key)

        articles = client.search_articles("trump")
        
        expected_article = [{
                "webPublicationDate": "2025-09-24T11:15:59Z",
                "webTitle": "Trump says he ‘can’t believe’ Kimmel back on ABC as he hints at action against network – US politics live",
                "webUrl": "https://www.theguardian.com/us-news/live/2025/sep/24/donald-trump-jimmy-kimmel-freedom-of-speech-immigration-government-shutdown-us-politics-live-news-updates",
            },
            {
                "webPublicationDate": "2025-09-24T11:02:21Z",
                "webTitle": "‘No alternative’ to continuing invasion, claims Russia, as Trump says Ukraine could regain all land lost – latest updates",
                "webUrl": "https://www.theguardian.com/world/live/2025/sep/24/russia-ukraine-trump-zelenskyy-unga-drones-europe-latest-news-updates",
            },
            {
                "webPublicationDate": "2025-09-24T11:01:04Z",
                "webTitle": "Trump looms large at Ryder Cup where home rules and spicy support are always on show",
                "webUrl": "https://www.theguardian.com/sport/2025/sep/24/trump-ryder-cup-spicy-support-use-europe-golf",
            },
            {
                "webPublicationDate": "2025-09-24T11:00:07Z",
                "webTitle": "Trump’s Tylenol announcement incurs furious backlash: ‘This is yet more utter rubbish’",
                "webUrl": "https://www.theguardian.com/us-news/2025/sep/24/trump-tylenol-pregnancy-autism-backlash",
            }
        ]

        assert articles == expected_article


###### Lambda Handler Tests ######


@patch('src.extract.boto3.client')
@patch.dict('os.environ', {'GUARDIAN_API_KEY': 'test-key'})
@patch('src.extract.requests.get')
def test_lambda_handler_adds_api_key(mock_get, _mock_boto, mock_guardian_api_one_response):
    # Arrange
    mock_response = Mock()
    mock_response.json.return_value = mock_guardian_api_one_response
    mock_get.return_value = mock_response

    #Act
    event = {'search_term': 'Warickshire'}
    lambda_handler(event, None)
    
    assert mock_get.called    
    called_url = mock_get.call_args[0][0]
    assert "&api-key=test-key" in called_url
    

@patch('src.extract.boto3.client')
@patch.dict('os.environ', {'GUARDIAN_API_KEY': 'test-key'})
@patch('src.extract.requests.get')
def test_lambda_handler_uses_search_term_from_event(mock_get, _mock_boto, mock_guardian_api_one_response):
    
    # Arrange
        mock_response = Mock()
        mock_response.json.return_value = mock_guardian_api_one_response
        mock_get.return_value = mock_response

        #Act
        event = {'search_term': 'Warickshire'}
        lambda_handler(event, None)

        #Assert
        called_url = mock_get.call_args[0][0]
        assert '&q=Warickshire' in called_url

        
@patch('src.extract.boto3.client')
@patch.dict('os.environ', {'GUARDIAN_API_KEY': 'test-key'})
@patch('src.extract.requests.get')
def test_lambda_handler_default_search(mock_get, _mock_boto, mock_guardian_api_one_response):
    
        # Arrange
        mock_response = Mock()
        mock_response.json.return_value = mock_guardian_api_one_response
        mock_get.return_value = mock_response

        #Act
        #passed empty search to trigger default search
        event = {}
        lambda_handler(event, None)

        #Assert
        called_url = mock_get.call_args[0][0]
        assert '&q=Northcoders' in called_url


# def test_lambda_handler_sends_single_articles_to_sqs()

# test_lambda_handler_sends_multiple_articles_to_sqs()

# test_error_handling - need to define what this is. 
