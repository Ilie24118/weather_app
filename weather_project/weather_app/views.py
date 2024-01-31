from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .models import City
from .forms import CityForm

import requests

# Create your views here.
from .forms import CityForm

# OpenWeatherMap API Token
api_token = ""


@login_required(login_url="login")
def index(request):
    form = CityForm()

    if request.method == "POST":
        form = CityForm({"name": request.POST["name"], "owner": request.user})

        if form.is_valid():
            city = form.cleaned_data["name"]

            url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}"

            city_weather = requests.get(url.format(city, api_token)).json()

            if city_weather["cod"] == "404":
                messages.info(request, "Can't find location. Try Again")
            else:
                form.save()
        else:
            pass

    cities = City.objects.values("owner", "name")

    weather_data = []
    forecast_data = []

    city_data = []

    for data in cities:
        if request.user.id == data["owner"]:
            city_data.append(data["name"])

    if not city_data:
        return render(request, "empty_base.html", {"form": form})

    for city in city_data:
        url = (
            "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}"
        )

        city_weather = requests.get(url.format(city, api_token)).json()

        weather = {
            "city": city,
            "temperature": city_weather["main"]["temp"],
            "descreption": city_weather["weather"][0]["description"],
            "icon": city_weather["weather"][0]["icon"],
        }
        weather_data.append(weather)

        context = {"weather_data": weather_data, "form": form}

    return render(request, "base.html", context)


def registerPage(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")

    context = {"form": form}

    return render(request, "register.html", context)


def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.info(request, "Username or Password incorrect")

    context = {}

    return render(request, "login.html", context)


def logoutUser(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def weatherForecast(request, city):
    weather_data = []
    forecast_data = []

    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}"
    fore_cast_url = (
        "https://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&appid={}"
    )

    city_weather = requests.get(url.format(city, api_token)).json()
    city_weather_forecast = requests.get(fore_cast_url.format(city, api_token)).json()

    weather = {
        "city": city,
        "temperature": city_weather["main"]["temp"],
        "descreption": city_weather["weather"][0]["description"],
        "icon": city_weather["weather"][0]["icon"],
    }
    weather_data.append(weather)

    for data in city_weather_forecast["list"][::8]:
        forecast = {
            "date": data["dt_txt"][:10],
            "temp": data["main"]["temp"],
            "descreption": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"],
        }
        forecast_data.append(forecast)
    context = {
        "weather_data": weather_data,
        "forecast": forecast_data,
    }

    if request.method == "POST":
        City.objects.filter(owner=request.user.id, name=city).delete()
        return redirect("home")

    return render(request, "weather_forecast.html", context)
