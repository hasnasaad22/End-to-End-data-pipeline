import requests

api_key = "YOUR_REAL_API_KEY"
api_url = f"http://api.weatherstack.com/current?access_key={api_key}&query=New York"


def fetch_weather():
    try:
        response = requests.get(api_url, timeout=5)
        data = response.json()

        # check if API returned error
        if "error" in data:
            print("API returned error:", data["error"])
            return None

        return data

    except Exception as e:
        print("API ERROR:", e)
        return None