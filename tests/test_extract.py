import pytest
import requests
from datetime import datetime
import json
from src.extract import GuardianAPI
from unittest.mock import patch, Mock


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


@pytest.fixture
def mock_guardian_api_limited_responses(): 
    return {
  "response": {
    "status": "ok",
    "userTier": "developer",
    "total": 92128,
    "startIndex": 1,
    "pageSize": 20,
    "currentPage": 1,
    "pages": 4607,
    "orderBy": "newest",
    "results": [
      {
        "id": "us-news/2025/sep/25/house-democrats-trump-palestinian-statehood",
        "type": "article",
        "sectionId": "us-news",
        "sectionName": "US news",
        "webPublicationDate": "2025-09-25T12:00:37Z",
        "webTitle": "House Democrats to send letter to Trump on Friday urging US to recognize Palestinian statehood",
        "webUrl": "https://www.theguardian.com/us-news/2025/sep/25/house-democrats-trump-palestinian-statehood",
        "apiUrl": "https://content.guardianapis.com/us-news/2025/sep/25/house-democrats-trump-palestinian-statehood",
        "isHosted": false,
        "pillarId": "pillar/news",
        "pillarName": "News"
      },
      {
        "id": "us-news/2025/sep/25/imam-freed-trump-deportation-cincinnati",
        "type": "article",
        "sectionId": "us-news",
        "sectionName": "US news",
        "webPublicationDate": "2025-09-25T12:00:36Z",
        "webTitle": "‘I was reborn’: Cincinnati imam reflects on 10 weeks in Ice custody after release",
        "webUrl": "https://www.theguardian.com/us-news/2025/sep/25/imam-freed-trump-deportation-cincinnati",
        "apiUrl": "https://content.guardianapis.com/us-news/2025/sep/25/imam-freed-trump-deportation-cincinnati",
        "isHosted": false,
        "pillarId": "pillar/news",
        "pillarName": "News"
      },
      {
        "id": "us-news/live/2025/sep/25/donald-trump-james-comey-fbi-ice-texas-latest-us-politics-news-updates-live",
        "type": "liveblog",
        "sectionId": "us-news",
        "sectionName": "US news",
        "webPublicationDate": "2025-09-25T11:54:30Z",
        "webTitle": "Former FBI director James Comey expected to be indicted on criminal charges, reports say – US politics live",
        "webUrl": "https://www.theguardian.com/us-news/live/2025/sep/25/donald-trump-james-comey-fbi-ice-texas-latest-us-politics-news-updates-live",
        "apiUrl": "https://content.guardianapis.com/us-news/live/2025/sep/25/donald-trump-james-comey-fbi-ice-texas-latest-us-politics-news-updates-live",
        "isHosted": false,
        "pillarId": "pillar/news",
        "pillarName": "News"
      },
      {
        "id": "world/2025/sep/25/is-trump-right-that-russian-economy-is-on-brink-of-collapse",
        "type": "article",
        "sectionId": "world",
        "sectionName": "World news",
        "webPublicationDate": "2025-09-25T11:36:46Z",
        "webTitle": "Is Trump right that Russia’s economy is on the brink of collapse?",
        "webUrl": "https://www.theguardian.com/world/2025/sep/25/is-trump-right-that-russian-economy-is-on-brink-of-collapse",
        "apiUrl": "https://content.guardianapis.com/world/2025/sep/25/is-trump-right-that-russian-economy-is-on-brink-of-collapse",
        "isHosted": false,
        "pillarId": "pillar/news",
        "pillarName": "News"
      },
      {
        "id": "us-news/2025/sep/25/ice-immigration-rodney-taylor-georgia",
        "type": "article",
        "sectionId": "us-news",
        "sectionName": "US news",
        "webPublicationDate": "2025-09-25T11:00:36Z",
        "webTitle": "Petition by man against Ice custody may provide new path to release for others",
        "webUrl": "https://www.theguardian.com/us-news/2025/sep/25/ice-immigration-rodney-taylor-georgia",
        "apiUrl": "https://content.guardianapis.com/us-news/2025/sep/25/ice-immigration-rodney-taylor-georgia",
        "isHosted": false,
        "pillarId": "pillar/news",
        "pillarName": "News"
      },
      {
        "id": "us-news/2025/sep/25/trump-cdc-budget-cuts-chronic-illness",
        "type": "article",
        "sectionId": "us-news",
        "sectionName": "US news",
        "webPublicationDate": "2025-09-25T11:00:35Z",
        "webTitle": "Trump’s CDC cuts could threaten chronic illness and national security, experts warn",
        "webUrl": "https://www.theguardian.com/us-news/2025/sep/25/trump-cdc-budget-cuts-chronic-illness",
        "apiUrl": "https://content.guardianapis.com/us-news/2025/sep/25/trump-cdc-budget-cuts-chronic-illness",
        "isHosted": false,
        "pillarId": "pillar/news",
        "pillarName": "News"
      },
      {
        "id": "tv-and-radio/2025/sep/25/theyve-finally-gone-there-south-park-lets-rip-at-benjamin-netanyahu",
        "type": "article",
        "sectionId": "tv-and-radio",
        "sectionName": "Television & radio",
        "webPublicationDate": "2025-09-25T10:52:58Z",
        "webTitle": "They’ve finally gone there: South Park lets rip at Benjamin Netanyahu",
        "webUrl": "https://www.theguardian.com/tv-and-radio/2025/sep/25/theyve-finally-gone-there-south-park-lets-rip-at-benjamin-netanyahu",
        "apiUrl": "https://content.guardianapis.com/tv-and-radio/2025/sep/25/theyve-finally-gone-there-south-park-lets-rip-at-benjamin-netanyahu",
        "isHosted": false,
        "pillarId": "pillar/arts",
        "pillarName": "Arts"
      },
      {
        "id": "us-news/2025/sep/25/first-thing-one-dead-and-two-injured-in-shooting-at-texas-ice-facility",
        "type": "article",
        "sectionId": "us-news",
        "sectionName": "US news",
        "webPublicationDate": "2025-09-25T10:21:02Z",
        "webTitle": "One dead and two injured in shooting at Texas Ice facility | First Thing",
        "webUrl": "https://www.theguardian.com/us-news/2025/sep/25/first-thing-one-dead-and-two-injured-in-shooting-at-texas-ice-facility",
        "apiUrl": "https://content.guardianapis.com/us-news/2025/sep/25/first-thing-one-dead-and-two-injured-in-shooting-at-texas-ice-facility",
        "isHosted": false,
        "pillarId": "pillar/news",
        "pillarName": "News"
      },
      {
        "id": "world/2025/sep/25/canada-ostrich-culling-bird-flu-protest",
        "type": "article",
        "sectionId": "world",
        "sectionName": "World news",
        "webPublicationDate": "2025-09-25T10:00:35Z",
        "webTitle": "Canada: order to cull over 400 ostriches sparks death threats for local businesses",
        "webUrl": "https://www.theguardian.com/world/2025/sep/25/canada-ostrich-culling-bird-flu-protest",
        "apiUrl": "https://content.guardianapis.com/world/2025/sep/25/canada-ostrich-culling-bird-flu-protest",
        "isHosted": false,
        "pillarId": "pillar/news",
        "pillarName": "News"
      },
      {
        "id": "football/2025/sep/25/zohran-mamdani-fifa-left-progressive-politics-sports",
        "type": "article",
        "sectionId": "football",
        "sectionName": "Football",
        "webPublicationDate": "2025-09-25T10:00:34Z",
        "webTitle": "Zohran Mamdani’s Fifa fight is a blueprint for the left to re-engage with sports | Leander Schaerlaeckens",
        "webUrl": "https://www.theguardian.com/football/2025/sep/25/zohran-mamdani-fifa-left-progressive-politics-sports",
        "apiUrl": "https://content.guardianapis.com/football/2025/sep/25/zohran-mamdani-fifa-left-progressive-politics-sports",
        "isHosted": false,
        "pillarId": "pillar/sport",
        "pillarName": "Sport"
      },
      {
        "id": "commentisfree/2025/sep/25/us-stock-market-trump-wall-street-financial-crisis-federal-reserve",
        "type": "article",
        "sectionId": "commentisfree",
        "sectionName": "Opinion",
        "webPublicationDate": "2025-09-25T10:00:34Z",
        "webTitle": "The next big financial crisis may be brewing. Warning signs are already there | Larry Elliott",
        "webUrl": "https://www.theguardian.com/commentisfree/2025/sep/25/us-stock-market-trump-wall-street-financial-crisis-federal-reserve",
        "apiUrl": "https://content.guardianapis.com/commentisfree/2025/sep/25/us-stock-market-trump-wall-street-financial-crisis-federal-reserve",
        "isHosted": false,
        "pillarId": "pillar/opinion",
        "pillarName": "Opinion"
      },
      {
        "id": "commentisfree/2025/sep/25/gaza-vessel-global-sumud-flotilla",
        "type": "article",
        "sectionId": "commentisfree",
        "sectionName": "Opinion",
        "webPublicationDate": "2025-09-25T10:00:34Z",
        "webTitle": "We are sailing to Gaza. Here’s why | David Adler",
        "webUrl": "https://www.theguardian.com/commentisfree/2025/sep/25/gaza-vessel-global-sumud-flotilla",
        "apiUrl": "https://content.guardianapis.com/commentisfree/2025/sep/25/gaza-vessel-global-sumud-flotilla",
        "isHosted": false,
        "pillarId": "pillar/opinion",
        "pillarName": "Opinion"
      },
      {
        "id": "us-news/2025/sep/25/dallas-shooting-ice-facility",
        "type": "article",
        "sectionId": "us-news",
        "sectionName": "US news",
        "webPublicationDate": "2025-09-25T10:00:33Z",
        "webTitle": "Deadly Ice shooting comes as violence spikes amid Trump immigration crackdown",
        "webUrl": "https://www.theguardian.com/us-news/2025/sep/25/dallas-shooting-ice-facility",
        "apiUrl": "https://content.guardianapis.com/us-news/2025/sep/25/dallas-shooting-ice-facility",
        "isHosted": false,
        "pillarId": "pillar/news",
        "pillarName": "News"
      },
      {
        "id": "australia-news/2025/sep/25/burwood-sydney-north-melbourne-among-world-coolest-neighbourhoods-time-out",
        "type": "article",
        "sectionId": "australia-news",
        "sectionName": "Australia news",
        "webPublicationDate": "2025-09-25T08:49:22Z",
        "webTitle": "Sydney’s Burwood and North Melbourne among world’s coolest neighbourhoods, Time Out says",
        "webUrl": "https://www.theguardian.com/australia-news/2025/sep/25/burwood-sydney-north-melbourne-among-world-coolest-neighbourhoods-time-out",
        "apiUrl": "https://content.guardianapis.com/australia-news/2025/sep/25/burwood-sydney-north-melbourne-among-world-coolest-neighbourhoods-time-out",
        "isHosted": false,
        "pillarId": "pillar/news",
        "pillarName": "News"
      },
      {
        "id": "fashion/2025/sep/25/fashion-livia-giuggioli-colin-firth-shreds-mbe-trump-uk-visit",
        "type": "article",
        "sectionId": "fashion",
        "sectionName": "Fashion",
        "webPublicationDate": "2025-09-25T08:48:57Z",
        "webTitle": "Fashion campaigner Livia Giuggioli shreds MBE over Trump’s ‘grotesque’ UK visit",
        "webUrl": "https://www.theguardian.com/fashion/2025/sep/25/fashion-livia-giuggioli-colin-firth-shreds-mbe-trump-uk-visit",
        "apiUrl": "https://content.guardianapis.com/fashion/2025/sep/25/fashion-livia-giuggioli-colin-firth-shreds-mbe-trump-uk-visit",
        "isHosted": false,
        "pillarId": "pillar/lifestyle",
        "pillarName": "Lifestyle"
      },
      {
        "id": "australia-news/live/2025/sep/25/australia-news-live-penny-wong-anthony-albanese-climate-crisis-united-nations-donald-trump-turkey-cop-politics-ntwnfb",
        "type": "liveblog",
        "sectionId": "australia-news",
        "sectionName": "Australia news",
        "webPublicationDate": "2025-09-25T08:16:41Z",
        "webTitle": "DNA tests to determine if heart belongs to man who died in Bali – as it happened",
        "webUrl": "https://www.theguardian.com/australia-news/live/2025/sep/25/australia-news-live-penny-wong-anthony-albanese-climate-crisis-united-nations-donald-trump-turkey-cop-politics-ntwnfb",
        "apiUrl": "https://content.guardianapis.com/australia-news/live/2025/sep/25/australia-news-live-penny-wong-anthony-albanese-climate-crisis-united-nations-donald-trump-turkey-cop-politics-ntwnfb",
        "isHosted": false,
        "pillarId": "pillar/news",
        "pillarName": "News"
      },
      {
        "id": "australia-news/2025/sep/25/brisbane-kindergarten-craigslea-proposed-charging-parents-2200-for-their-own-childrens-art-forced-to-back-down",
        "type": "article",
        "sectionId": "australia-news",
        "sectionName": "Australia news",
        "webPublicationDate": "2025-09-25T08:04:01Z",
        "webTitle": "Brisbane kindergarten forced to back down after proposing to charge parents $2,200 for their own children’s art",
        "webUrl": "https://www.theguardian.com/australia-news/2025/sep/25/brisbane-kindergarten-craigslea-proposed-charging-parents-2200-for-their-own-childrens-art-forced-to-back-down",
        "apiUrl": "https://content.guardianapis.com/australia-news/2025/sep/25/brisbane-kindergarten-craigslea-proposed-charging-parents-2200-for-their-own-childrens-art-forced-to-back-down",
        "isHosted": false,
        "pillarId": "pillar/news",
        "pillarName": "News"
      },
      {
        "id": "australia-news/2025/sep/25/new-ndis-assessments-using-technology-simplify-process-advocacy-groups-hesitant-about-change",
        "type": "article",
        "sectionId": "australia-news",
        "sectionName": "Australia news",
        "webPublicationDate": "2025-09-25T07:37:41Z",
        "webTitle": "New NDIS needs assessments will use technology to simplify process but advocacy groups cautious about change",
        "webUrl": "https://www.theguardian.com/australia-news/2025/sep/25/new-ndis-assessments-using-technology-simplify-process-advocacy-groups-hesitant-about-change",
        "apiUrl": "https://content.guardianapis.com/australia-news/2025/sep/25/new-ndis-assessments-using-technology-simplify-process-advocacy-groups-hesitant-about-change",
        "isHosted": false,
        "pillarId": "pillar/news",
        "pillarName": "News"
      },
      {
        "id": "australia-news/2025/sep/25/afternoon-update-thursday-ntwnfb",
        "type": "article",
        "sectionId": "australia-news",
        "sectionName": "Australia news",
        "webPublicationDate": "2025-09-25T06:51:20Z",
        "webTitle": "Afternoon Update: PM urges UN to unite; Bali hospital denies alleged organ theft; and recipes for the footy final",
        "webUrl": "https://www.theguardian.com/australia-news/2025/sep/25/afternoon-update-thursday-ntwnfb",
        "apiUrl": "https://content.guardianapis.com/australia-news/2025/sep/25/afternoon-update-thursday-ntwnfb",
        "isHosted": false,
        "pillarId": "pillar/news",
        "pillarName": "News"
      },
      {
        "id": "australia-news/2025/sep/25/victoria-crime-rate-increase-up-theft-family-violence",
        "type": "article",
        "sectionId": "australia-news",
        "sectionName": "Australia news",
        "webPublicationDate": "2025-09-25T06:44:09Z",
        "webTitle": "Less than 1% of population responsible for 40% of all offending in Victoria as crime rate climbs",
        "webUrl": "https://www.theguardian.com/australia-news/2025/sep/25/victoria-crime-rate-increase-up-theft-family-violence",
        "apiUrl": "https://content.guardianapis.com/australia-news/2025/sep/25/victoria-crime-rate-increase-up-theft-family-violence",
        "isHosted": false,
        "pillarId": "pillar/news",
        "pillarName": "News"
      }
    ]
  }
}

# API test key variable
test_key = "test"



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
    # No search query added
    client.search_articles("Warickshire")
    called_url = mock_get.call_args[0][0]

    # Check URL has &
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






 

