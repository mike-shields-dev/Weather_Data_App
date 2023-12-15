import os
import requests
from dotenv import load_dotenv
load_dotenv()

async def get_weather_data(geolocation):
    [latitude, longitude] = geolocation

    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    WEATHER_API_HOST = os.getenv("WEATHER_API_HOST")
    BASE_URL = "https://" + WEATHER_API_HOST
    URL = BASE_URL + "/current.json"

    headers = {
        "X-RapidAPI-Key": WEATHER_API_KEY,
        "X-RapidAPI-Host": WEATHER_API_HOST,
    }

    querystring = {"q": f"{latitude}, {longitude}"}

    try:
        response = requests.get(url=URL, headers=headers, params=querystring)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()

        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data for LOCATION: {str(e)}")

        return None
