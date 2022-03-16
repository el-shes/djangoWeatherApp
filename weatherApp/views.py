import requests
from django.shortcuts import render


# Create your views here.
from .models import City


def weather_view(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units={}&appid=110a6ca59b063163742ebf7ff21d3e04'
    city = 'Shanghai'

    weather_data = []

    cities = City.objects.all()
    for city in cities:

        r = requests.get(url.format(city, 'metric')).json()

        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }
        weather_data.append(city_weather)

    context = {'weather_data': weather_data}

    return render(request, 'weatherApp/weather.html', context)
