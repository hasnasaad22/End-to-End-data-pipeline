import requests

api_key = "aa8ccf004c0ca38e4196a03ae5f8d48a"
api_url = f"http://api.weatherstack.com/current?access_key={api_key}&query=New York"


def mock_fetch_data():
    return {
        'request': {
            'type': 'City',
            'query': 'New York, United States of America',
            'language': 'en',
            'unit': 'm'
        },
        'location': {
            'name': 'New York',
            'country': 'United States'
        }
    }