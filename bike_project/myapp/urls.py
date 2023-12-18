# myapp/urls.py

from django.urls import path
from myapp.views import fetch_bike_data, bike_station_shortages, bike_station_predictions, fetch_bike_data_view, fetch_weather_data, fetch_learning_data
from . import views
urlpatterns = [
    # path('bike-stations/', save_data, name='save_data'),
    path('bike-stations/', bike_station_shortages, name='bike_station_shortages'),
    path('bike-stations/', bike_station_predictions, name='bike_station_predictions'),
    path('bike-stations/', fetch_bike_data_view, name='fetch_bike_data_view'),
    path('fetch-learning-data/', fetch_learning_data, name='fetch_learning_data'),
    path('fetch-bike-data/', fetch_bike_data, name='fetch_bike_data'),
    path('fetch-weather-data/', fetch_weather_data, name='fetch_weather_data'),
]
