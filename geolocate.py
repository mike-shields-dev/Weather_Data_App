import os
import geocoder
import httpx
from dotenv import load_dotenv

from get_user_selection import *

# intentionally global
geolocation_method_options = ["From my IP address", "Provide place name"]


async def get_user_geolocation_method_selection():
    selected_geolocation_method = await get_user_selection(
        topic="geolocation_selection",
        message="What method would you like to use to get Weather Data?",
        choices=geolocation_method_options,
    )

    return selected_geolocation_method


async def get_coordinates(geolocation_method):
    if geolocation_method == geolocation_method_options[0]:
        return get_coordinates_from_ip_address()
    elif geolocation_method == geolocation_method_options[1]:
        return await get_coordinates_from_place_name()
    else:
        return get_coordinates_from_ip_address()


def get_coordinates_from_ip_address():
    g = geocoder.ip("me")

    return g.latlng


async def get_coordinates_from_place_name():
    place = await get_user_selected_place_data()

    return [place["lat"], place["lon"]]


def format_place(place):
    return f"{place['name']}, {place['region']}, {place['country']}"

async def get_user_place_selection(places):
    formatted_places = {format_place(place): place for place in places}
    places_options = list(formatted_places.keys())

    selected_place = await get_user_selection(
        topic="selected_place",
        message="Multiple matches found, please choose one",
        choices=places_options,
    )

    return formatted_places.get(selected_place)


async def fetch_places(place_name, headers, SEARCH_URL):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                SEARCH_URL, headers=headers, params={"q": place_name}
            )
            return response.json()
        except httpx.RequestError as e:
            print(f"Error fetching data, please try again: {str(e)}")
            return []

async def get_user_selected_place_data():
    load_dotenv()
    
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    WEATHER_API_HOST = os.getenv("WEATHER_API_HOST")
    BASE_URL = f"https://{WEATHER_API_HOST}"
    SEARCH_URL = f"{BASE_URL}/search.json"

    headers = {
        "X-RapidAPI-Key": WEATHER_API_KEY,
        "X-RapidAPI-Host": WEATHER_API_HOST,
    }

    while True:
        place_name = input("Please enter place name:\n")
        places = await fetch_places(place_name, headers, SEARCH_URL)

        if len(places) == 0:
            print("No matches found, please try entering place name again.")
        elif len(places) == 1:
            return places[0]
        else:
            return await get_user_place_selection(places)