# myapp/urls.py

from django.urls import path
from myapp.views import fetch_bike_data, bike_station_shortages, bike_station_predictions, fetch_bike_data_view, load_prediction_data

urlpatterns = [
    path('bike-stations/', bike_station_shortages, name='bike_station_shortages'),
    path('bike-stations/', bike_station_predictions, name='bike_station_predictions'),
    path('bike-stations/', fetch_bike_data_view, name='fetch_bike_data_view'),
    path('fetch-bike-data/', fetch_bike_data, name='fetch_bike_data'),
    path('bike-stations/', load_prediction_data, name='load_prediction_data'),
]
