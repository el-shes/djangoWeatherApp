import requests
from django.shortcuts import render, redirect

# Create your views here.
from .models import City
from .forms import CityForm


def weather_view(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units={}&appid=110a6ca59b063163742ebf7ff21d3e04'
    city = 'Shanghai'

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
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }
        weather_data.append(city_weather)

    context = {'weather_data': weather_data, 'form': form, 'message': user_message, 'message_class': message_class}

    return render(request, 'weatherApp/weather.html', context)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')
