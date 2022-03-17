
from django.urls import path
from . import views

urlpatterns = [
    path('', views.weather_view, name='home'),
    path('delete/<city_name>/', views.delete_city, name='delete_city')
]