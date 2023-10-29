import os
import geocoder
import inquirer
import httpx
from dotenv import load_dotenv
load_dotenv()

geolocation_method_options = [
    "From my IP address",
    "Provide place name"
]


def select_geolocation_method():
    question = [
        inquirer.List(
            "location_method",
            message="What method would you like to use to get weather data?",
            choices=geolocation_method_options
        ),
    ]

    choices = inquirer.prompt(question)
    locate_method = choices["location_method"]

    return locate_method


def from_ip():
    g = geocoder.ip("me")

    return g.latlng


def select_location(locations):
    options = [
        f"{loc['name']}, {loc['region']}, {loc['country']}" for loc in locations]

    question = [
        inquirer.List(
            "selected_location",
            message="Multiple matches found, please choose one",
            choices=options,
        )
    ]

    answers = inquirer.prompt(question)
    selected_location = answers["selected_location"]

    for location in locations:
        if selected_location == f"{location['name']}, {location['region']}, {location['country']}":
            return location


async def get_location():
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    WEATHER_API_HOST = os.getenv("WEATHER_API_HOST")
    BASE_URL = "https://" + WEATHER_API_HOST
    SEARCH_URL = BASE_URL + "/search.json"

    headers = {
        "X-RapidAPI-Key": WEATHER_API_KEY,
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }

    search_term = input("Please enter place name:\n")

    async with httpx.AsyncClient() as client:
        while True:
            try:
                response = await client.get(
                    SEARCH_URL,
                    headers=headers,
                    params={"q": search_term}
                )

                found_locations = response.json()

                if len(found_locations) == 0:
                    search_term = input("No matches found, please try entering place name again \n")
                if len(found_locations) == 1:
                    return found_locations[0]
                if len(found_locations) > 1:
                    return select_location(found_locations)

            except httpx.RequestError as e:
                print(f"Error fetching data, please try again: {str(e)}")


async def from_place_name():
    loc = await get_location()

    return [loc["lat"], loc["lon"]]

async def geolocate(geolocation_method):
    geolocation = None

    if geolocation_method == geolocation_method_options[0]:
        geolocation = from_ip()
    elif geolocation_method == geolocation_method_options[1]:
        geolocation = await from_place_name()
    else:
        geolocation = from_ip()

    return geolocation
