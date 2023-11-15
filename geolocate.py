import os
import geocoder
import inquirer
import httpx
from dotenv import load_dotenv

load_dotenv()

geolocation_method_options = ["From my IP address", "Provide place name"]


def get_user_geolocation_method_selection():
    question = [
        inquirer.List(
            "geolocation_method",
            message="What geolocation method would you like to use to get weather data?",
            choices=geolocation_method_options,
        ),
    ]

    choices = inquirer.prompt(question)
    locate_method = choices["geolocation_method"]

    return locate_method


async def get_coordinates(geolocation_method):
    if geolocation_method == geolocation_method_options[0]:
        return get_coordinates_from_ip_address()
    elif geolocation_method == geolocation_method_options[1]:
        return await get_coords_from_place_name()
    else:
        return get_coordinates_from_ip_address()


def get_coordinates_from_ip_address():
    g = geocoder.ip("me")

    return g.latlng


async def get_coords_from_place_name():
    place = await get_desired_place()

    return [place["lat"], place["lon"]]


def get_user_place_selection(places):
    options = [
        f"{place['name']}, {place['region']}, {place['country']}" for place in places
    ]

    question = [
        inquirer.List(
            "selected_location",
            message="Multiple matches found, please choose one",
            choices=options,
        )
    ]

    answers = inquirer.prompt(question)
    selected_location = answers["selected_location"]

    for place in places:
        if (
            selected_location
            == f"{place['name']}, {place['region']}, {place['country']}"
        ):
            return place


async def get_desired_place():
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    WEATHER_API_HOST = os.getenv("WEATHER_API_HOST")
    BASE_URL = "https://" + WEATHER_API_HOST
    SEARCH_URL = BASE_URL + "/search.json"

    headers = {
        "X-RapidAPI-Key": WEATHER_API_KEY,
        "X-RapidAPI-Host": WEATHER_API_HOST,
    }

    place_name = input("Please enter place name:\n")

    async with httpx.AsyncClient() as client:
        while True:
            try:
                response = await client.get(
                    SEARCH_URL, headers=headers, params={"q": place_name}
                )

                matching_place_names = response.json()

                if len(matching_place_names) == 0:
                    place_name = input(
                        "No matches found, please try entering place name again \n"
                    )
                if len(matching_place_names) == 1:
                    return matching_place_names[0]
                if len(matching_place_names) > 1:
                    return get_user_place_selection(matching_place_names)

            except httpx.RequestError as e:
                print(f"Error fetching data, please try again: {str(e)}")
