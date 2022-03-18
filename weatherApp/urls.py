
from django.urls import path
from . import views

urlpatterns = [
    path('', views.weather_view, name='home'),
    path('delete/<city_name>/', views.delete_city, name='delete_city'),
    path('forecast7?city_name=<city_name>&lon=<lon>&lat=<lat>', views.seven_days_weather, name='seven_days_weather')
]
