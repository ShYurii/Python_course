import aiohttp
from config import cfg

async def get_weather_by_coords(lat: float, lon: float) -> str:
    # Get weather from OpenWeather API by coordinates.
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={cfg.OPENWEATHER_TOKEN}&units=metric&lang=uk"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()

    if "main" not in data:
        return "Failed to get weather 😢"

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    city = data["name"]

    return f"Weather in {city}: {temp}°C, {desc}"



async def get_weather_by_city(city: str) -> str:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={cfg.OPENWEATHER_TOKEN}&units=metric&lang=uk"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()

    if "main" not in data:
        return "Не вдалося отримати погоду 😢"

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    city_name = data["name"]
    return f"Погода у {city_name}: {temp}°C, {desc}"

