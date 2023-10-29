from geolocate import select_geolocation_method, geolocate
from weather_data import *
from weather_data import *
from pretty_print_json import *

async def main():
    geolocation_method = select_geolocation_method()
    geolocation = await geolocate(geolocation_method)
    weather_data = await get_weather_data(geolocation)
    pretty_print_json(weather_data)
    exit()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
