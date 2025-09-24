import pytest
import requests
from datetime import datetime
import json
from src.extract import GuardianAPI
from unittest.mock import patch, Mock


# ===== fixtures & variables =====

# Fixture of Guardian API response used for mocking.
@pytest.fixture
def mock_guardian_api_response(): 
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
            "id": "world/live/2025/sep/24/typhoon-ragasa-live-china-hong-kong-taiwan-philippines-latest-storm-news-updates",
            "type": "liveblog",
            "sectionId": "world",
            "sectionName": "World news",
            "webPublicationDate": "2025-09-24T11:14:40Z",
            "webTitle": "Typhoon Ragasa live: deadly cyclone makes landfall in China after devastating Hong Kong, Taiwan and Philippines",
            "webUrl": "https://www.theguardian.com/world/live/2025/sep/24/typhoon-ragasa-live-china-hong-kong-taiwan-philippines-latest-storm-news-updates",
            "apiUrl": "https://content.guardianapis.com/world/live/2025/sep/24/typhoon-ragasa-live-china-hong-kong-taiwan-philippines-latest-storm-news-updates",
            "isHosted": False,
            "pillarId": "pillar/news",
            "pillarName": "News"
        },
        {
            "id": "technology/2025/sep/24/adviser-uk-minister-claimed-ai-firms-never-compensate-creatives",
            "type": "article",
            "sectionId": "technology",
            "sectionName": "Technology",
            "webPublicationDate": "2025-09-24T11:07:45Z",
            "webTitle": "Adviser to UK minister claimed AI firms will never have to compensate creatives",
            "webUrl": "https://www.theguardian.com/technology/2025/sep/24/adviser-uk-minister-claimed-ai-firms-never-compensate-creatives",
            "apiUrl": "https://content.guardianapis.com/technology/2025/sep/24/adviser-uk-minister-claimed-ai-firms-never-compensate-creatives",
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
            "id": "politics/live/2025/sep/24/labour-tories-conservatives-reform-uk-politics-live-news-updates",
            "type": "liveblog",
            "sectionId": "politics",
            "sectionName": "Politics",
            "webPublicationDate": "2025-09-24T11:01:40Z",
            "webTitle": "Royal Parks say no evidence to back Nigel Farage’s claim that migrants are eating their swans – UK politics live",
            "webUrl": "https://www.theguardian.com/politics/live/2025/sep/24/labour-tories-conservatives-reform-uk-politics-live-news-updates",
            "apiUrl": "https://content.guardianapis.com/politics/live/2025/sep/24/labour-tories-conservatives-reform-uk-politics-live-news-updates",
            "isHosted": False,
            "pillarId": "pillar/news",
            "pillarName": "News"
        },
        {
            "id": "music/2025/sep/24/as-a-15-year-old-funkateer-he-meant-the-world-to-me-chris-hill-influence-by-gilles-peterson",
            "type": "article",
            "sectionId": "music",
            "sectionName": "Music",
            "webPublicationDate": "2025-09-24T11:01:10Z",
            "webTitle": "The late DJ Chris Hill galvanised funkateers, brought Black music to the clubs – and got Mick Jones dancing ",
            "webUrl": "https://www.theguardian.com/music/2025/sep/24/as-a-15-year-old-funkateer-he-meant-the-world-to-me-chris-hill-influence-by-gilles-peterson",
            "apiUrl": "https://content.guardianapis.com/music/2025/sep/24/as-a-15-year-old-funkateer-he-meant-the-world-to-me-chris-hill-influence-by-gilles-peterson",
            "isHosted": False,
            "pillarId": "pillar/arts",
            "pillarName": "Arts"
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
        },
        {
            "id": "world/2025/sep/24/canada-sushi-shop-refuses-extra-soy-sauce",
            "type": "article",
            "sectionId": "world",
            "sectionName": "World news",
            "webPublicationDate": "2025-09-24T11:00:06Z",
            "webTitle": "Cry over spilt soy: Canada sushi shop refuses to dole out extra sauce for patrons",
            "webUrl": "https://www.theguardian.com/world/2025/sep/24/canada-sushi-shop-refuses-extra-soy-sauce",
            "apiUrl": "https://content.guardianapis.com/world/2025/sep/24/canada-sushi-shop-refuses-extra-soy-sauce",
            "isHosted": False,
            "pillarId": "pillar/news",
            "pillarName": "News"
        }
        ]
    }
    }

# API test key variable
test_key = "test-key"


# ===== TDD =====
# test_API_Key_Validation:
def test_guardian_api_retrieves_api_key():
    """Tests: accepts API key, covers any None/empty keys"""
    
    client = GuardianAPI(test_key)
    assert client.api_key == test_key

    # Rejects Empty
    with pytest.raises(ValueError, match="Valid API key is required"):
        GuardianAPI(api_key="")


# ===== Search Functionality =====

# Tests Search_articles GETS JSON response
@patch('src.extract.requests')  
def test_guardian_api_gets_article_data(mock_requests, mock_guardian_api_response):
    """Tests: that we are adding API key and pulling Guardian's JSON """

    mock_response = Mock()
    mock_response.json.return_value = mock_guardian_api_response
    mock_requests.get.return_value = mock_response

    client = GuardianAPI(test_key)

    articles = client.search_articles("test")
    # Uses first article of mock
    expected_article = {
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
        }

    assert articles[0] == expected_article


# Tests Search_articles searches via keyword
@patch('src.extract.requests')  
def test_search_articles_accepts_search_terms(mock_requests, mock_guardian_api_response):
    """Tests: search articles method - tests date & search terms"""

    mock_response = Mock()
    mock_response.json.return_value = mock_guardian_api_response
    mock_requests.get.return_value = mock_response

    client = GuardianAPI(test_key)

    articles = client.search_articles("Warwickshire")
    
    expected_article = {
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
        }

    assert articles[0] == expected_article



# ===== Processing of JSON Data =====

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
 

