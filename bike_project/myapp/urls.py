# myapp/urls.py

from django.urls import path
from myapp.views import fetch_bike_data, bike_number_prediction, bike_station_shortages,fetch_bike_data_view, fetch_weather_data, fetch_learning_data
# from myapp.views import save_data, bike_station_predictions
from . import views
urlpatterns = [
    path('', bike_station_shortages, name='bike_station_shortages'),
    path('', fetch_bike_data_view, name='fetch_bike_data_view'),
    path('fetch-learning-data/', fetch_learning_data, name='fetch_learning_data'),
    path('fetch-bike-data/', fetch_bike_data, name='fetch_bike_data'),
    path('fetch-weather-data/', fetch_weather_data, name='fetch_weather_data'),
    path('bike-number-prediction/', bike_number_prediction, name='bike_number_prediction'),
]
