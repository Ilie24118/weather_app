from django.forms import ModelForm, TextInput
from django import forms
from .models import City


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ["name", "owner"]

        widgets = {
            "name": TextInput(attrs={"class": "input", "placeholder": "City Name"})
        }
