import datetime

import requests
from django.shortcuts import render, redirect

# Create your views here.
from .models import City
from .forms import CityForm


def weather_view(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units={}&appid=110a6ca59b063163742ebf7ff21d3e04'

    err_msg = ''
    user_message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            # duplicate city check
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            if not existing_city_count:
                # checking valid city
                r = requests.get(url.format(new_city, 'metric')).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'City does not exist'
            else:
                err_msg = 'City already in the database'

        if err_msg:
            user_message = err_msg
            message_class = 'is-danger'
        else:
            user_message = 'City added successfully!'
            message_class = 'is-success'

    form = CityForm()

    weather_data = []

    cities = City.objects.all()
    for city in cities:

        r = requests.get(url.format(city, 'metric')).json()

        city_weather = {
            'city': city.name,
            'temperature': round(r['main']['temp']),
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
            'lon': r['coord']['lon'],
            'lat': r['coord']['lat'],
        }
        weather_data.append(city_weather)

    context = {'weather_data': weather_data, 'form': form, 'message': user_message, 'message_class': message_class}

    return render(request, 'weatherApp/weather.html', context)


def delete_city(request, city_name):
    if request.method == 'POST':
        City.objects.get(name=city_name).delete()
        return redirect('home')

    return render(request, 'weatherApp/weather_confirm_delete.html', {'city_name': city_name})


def seven_days_weather(request, lon, lat, city_name):
    url = 'https://api.openweathermap.org/data/2.5/onecall?lon={}&lat={' \
          '}&units=metric&appid=110a6ca59b063163742ebf7ff21d3e04&exclude=minutely,hourly '

    r = requests.get(url.format(lon, lat)).json()

    daily_info = []
    for day in r['daily']:
        daily_info.append({'day_of_week': datetime.datetime.fromtimestamp(day['dt']).strftime('%A'),
                           'date': datetime.datetime.fromtimestamp(day['dt']).date(),
                           'temp_day': round(day['temp']['day']),
                           'temp_night': round(day['temp']['night']),
                           'weather': day['weather'][0]['main'],
                           'description': day['weather'][0]['description'],
                           'icon': day['weather'][0]['icon']})

    return render(request, 'weatherApp/seven_days_weather.html', {'daily_info': daily_info, 'city_name': city_name})
