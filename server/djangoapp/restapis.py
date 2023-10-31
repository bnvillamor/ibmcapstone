import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from django.shortcuts import render


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, api_key=None, **kwargs):
    params = kwargs.get('params', {})
    if api_key:
        response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                auth=HTTPBasicAuth('apikey', api_key))
    else:
        response = requests.get(url, params=params)
    return response


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(dealer_id):
    cloud_function_url = 'https://us-south.functions.appdomain.cloud/api/v1/web/ac844fdd-a8a1-4ac3-9754-64c371ab61d1/dealership-package/getdealershipsbystate'
    api_key = None
    # Define the parameters to send with the GET request
    params = {'dealerId': dealer_id}

    try:
        response = requests.get(cloud_function_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()  # Parse the JSON response

        # Create a list of DealerReview objects from the JSON data
        reviews = []
        for item in data:
            review = DealerReview(
            dealership=item['dealership'],
            name=item['name'],
            purchase=item['purchase'],
            review=item['review'],
            purchase_date=item['purchase_date'],
            car_make=item['car_make'],
            car_model=item['car_model'],
            car_year=item['car_year'],
            sentiment=analyze_review_sentiments(item['review'], api_key),  # Analyze sentiment
            id=item['id']
        )
        reviews.append(review)
    
        return reviews

    except requests.exceptions.RequestException as e:
        # Handle request exceptions, e.g., connection errors, timeouts, etc.
        print(f"Error: {e}")
        return []

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text, api_key):
    url = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/your-instance-id/v1/analyze'
    params = {
        'text': text,
        'version': '2022-01-01',  # Use the appropriate version
        'features': 'sentiment',
        'return_analyzed_text': True
    }

    response = get_request(url, api_key=api_key, params=params)

    if response.status_code == 200:
        result = response.json()
        sentiment = result.get('sentiment', None)
        return sentiment
    else:
        return None


