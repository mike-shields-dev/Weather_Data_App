from geolocate import select_geolocation_method, geolocate
from weather_data import *
from weather_data import *

async def main():
    geolocation_method = select_geolocation_method()
    geolocation = await geolocate(geolocation_method)
    data = await get_weather_data(geolocation)
    
    print(data) 

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
