from rest_framework.response import Response
from rest_framework.decorators import api_view
from weather_app.models import City
from .serializers import CitySerializer

from django.contrib.auth.decorators import login_required

from weather_app.models import City

from weather_app.views import api_token

import requests


@login_required(login_url="login")
@api_view(["GET"])
def getData(request):
    cities = City.objects.all()
    serializer = CitySerializer(cities, many=True)

    return Response(serializer.data)


@login_required(login_url="login")
@api_view(["GET"])
def getSearch(request, city):
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}"

    city_weather = requests.get(url.format(city, api_token)).json()
    if city_weather["cod"] == "404":
        return Response({"cod": 404})

    weather_data = []

    weather = {
        "city": city,
        "temperature": city_weather["main"]["temp"],
        "descreption": city_weather["weather"][0]["description"],
    }

    weather_data.append(weather)

    return Response(weather)


@login_required(login_url="login")
@api_view(["GET"])
def getForecast(request, city):
    fore_cast_url = (
        "https://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&appid={}"
    )

    city_weather_forecast = requests.get(fore_cast_url.format(city, api_token)).json()

    if city_weather_forecast["cod"] == "404":
        return Response({"cod": 404})

    forecast_data = []

    for data in city_weather_forecast["list"][::8]:
        forecast = {
            "name": city,
            "date": data["dt_txt"][:10],
            "temp": data["main"]["temp"],
            "descreption": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"],
        }
        forecast_data.append(forecast)

    return Response(forecast_data)


@api_view(["GET"])
def getCurrent(request):
    cities = City.objects.values("owner", "name")

    city_data = []
    for data in cities:
        if request.user.id == data["owner"]:
            city_data.append(data["name"])

    weather_data = []
    for city in city_data:
        url = (
            "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}"
        )

        city_weather = requests.get(url.format(city, api_token)).json()

        weather = {
            "city": city,
            "temperature": city_weather["main"]["temp"],
            "descreption": city_weather["weather"][0]["description"],
        }
        weather_data.append(weather)

    return Response(weather_data)
