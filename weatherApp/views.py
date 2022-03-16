import requests
from django.shortcuts import render


# Create your views here.


def weather_view(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units={}&appid=110a6ca59b063163742ebf7ff21d3e04'
    city = 'Kyiv'

    r = requests.get(url.format(city, 'metric')).json()
    city_weather = {
        'city': city,
        'temperature': r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon'],
    }

    context = {'city_weather': city_weather}

    return render(request, 'weatherApp/weather.html', context)
