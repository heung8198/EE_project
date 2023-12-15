from django.db import models

class BikeStation(models.Model):
    station_name = models.CharField(max_length=100)
    parking_bike_count = models.IntegerField()
    total_rack_count = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    # 기타 필요한 필드 추가
