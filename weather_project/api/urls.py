from django.urls import path
from . import views

urlpatterns = [
    path("weather", views.getData),
    path("weather/search/<str:city>", views.getSearch),
    path("weather/forecast/<str:city>", views.getForecast),
    path("weather/current", views.getCurrent),
]
