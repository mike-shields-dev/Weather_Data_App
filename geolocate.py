import os
import geocoder
import inquirer
import requests_async as requests
import httpx
from dotenv import load_dotenv
load_dotenv()


def select_geolocation_method():
    questions = [
        inquirer.List(
            "location_method",
            message="What weather data would you like?",
            choices=[
                "1. My current geolocation (auto)",
                "2. Another geolocation (lat, long)",
                "3. An address"
            ]
        ),
    ]

    choices = inquirer.prompt(questions)
    locate_method = int(choices["location_method"][0], 10)

    return locate_method


def automatically():
    g = geocoder.ip("me")

    return g.latlng


def manually():
    latitude = None
    longitude = None

    while True:
        try:
            user_latitude = float(
                input("Please enter latitude and hit Enter\n"))
            if 0 <= user_latitude <= 90:
                latitude = user_latitude
                break
            else:
                print("latitude must be in the range 0 to 90")
        except ValueError:
            print("latitude must be a number in the range 0 to 90")

    while True:
        try:
            user_longitude = float(
                input("Please enter longitude and hit Enter\n"))
            if -180 <= user_longitude <= 180:
                longitude = user_longitude
                break
            else:
                print("longitude must be in the range -180 to 180")
        except ValueError:
            print("longitude must be a number in the range -180 to 180")

    return [latitude, longitude]


def select_search_term(places):
    place_choices = [
        f"{place['name']}, {place['region']}, {place['country']}"
        for place in places
    ]

    questions = [
        inquirer.List(
            "selected_place",
            message="Several places found, please choose one:",
            choices=place_choices
        ),
    ]

    results = inquirer.prompt(questions)
    selected_place = results["selected_place"]

    return selected_place


# async def get_location():
#     WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
#     WEATHER_API_HOST = os.getenv("WEATHER_API_HOST")
#     BASE_URL = "https://" + WEATHER_API_HOST
#     SEARCH_URL = BASE_URL + "/search.json"

#     headers = {
#         "X-RapidAPI-Key": WEATHER_API_KEY,
#         "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
#     }

#     selected_location = None

#     search_term = input("Please enter place name:\n")
    
#     while selected_location == None:
#         try:
#             response = await requests.get(
#                 url=SEARCH_URL,
#                 headers=headers,
#                 params={"q": search_term}
#             )

#             found_locations = response.json()

#             if len(found_locations) == 0:
#                 search_term = ("No matches found, please try again")
#             elif len(found_locations) == 1:
#                 selected_location = found_locations[0]
#             elif len(found_locations) > 1:
#                 search_term = select_search_term(found_locations)

#         except requests.exceptions.RequestException as e:
#             print(f"Error fetching data, please try again: {str(e)}")

#     return selected_location

async def get_location():
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    WEATHER_API_HOST = os.getenv("WEATHER_API_HOST")
    BASE_URL = "https://" + WEATHER_API_HOST
    SEARCH_URL = BASE_URL + "/search.json"

    headers = {
        "X-RapidAPI-Key": WEATHER_API_KEY,
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }

    selected_location = None

    search_term = input("Please enter place name:\n")

    async with httpx.AsyncClient() as client:
        while selected_location is None:
            try:
                response = await client.get(
                    SEARCH_URL,
                    headers=headers,
                    params={"q": search_term}
                )

                found_locations = response.json()

                if len(found_locations) == 0:
                    search_term = "No matches found, please try again"
                elif len(found_locations) == 1:
                    selected_location = found_locations[0]
                    break
                elif len(found_locations) > 1:
                    search_term = select_search_term(found_locations)
                    break

            except httpx.RequestError as e:
                print(f"Error fetching data, please try again: {str(e)}")

    return selected_location


async def from_place_name():
    location = await get_location()
    
    latitude, longitude = location["lat"], location["lon"]  
    print(latitude, longitude)

    return [0, 0]


async def geolocate(geolocation_method):
    geolocation = None

    if geolocation_method == 1:
        geolocation = automatically()
    elif geolocation_method == 2:
        geolocation = manually()
    elif geolocation_method == 3:
        geolocation = await from_place_name() if await from_place_name() is not None else [0,0]
    else:
        geolocation = automatically()

    return geolocation
