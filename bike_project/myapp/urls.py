# myapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.bike_stations, name='bike_stations'),  # 'bike_stations' 뷰를 URL 경로에 연결
    path('fetch-bike-data/', views.fetch_bike_data_view, name='fetch-bike-data'),
]
