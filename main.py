from geolocate import get_user_geolocation_method_selection, get_coordinates
from weather_data import *
from pretty_print_json import *
import asyncio

async def main():
    selected_geolocation_method = await get_user_geolocation_method_selection()
    coordinates = await get_coordinates(selected_geolocation_method)
    weather_data = await get_weather_data(coordinates)
    pretty_print_json(weather_data)
    
    exit()

asyncio.run(main())
