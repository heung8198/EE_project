from django.db import models

class BikeStation(models.Model):
    station_name = models.CharField(max_length=100)
    parking_bike_count = models.IntegerField()
    total_rack_count = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    # 기타 필요한 필드 추가

class PredictionBicycle(models.Model):
    station_name = models.CharField(max_length=100)
    rental_date = models.DateField()
    rental_hour = models.IntegerField()
    expected_usage = models.IntegerField()
    temperature = models.FloatField()
    wind_speed = models.FloatField()
    rainfall = models.FloatField()
    humidity = models.IntegerField()
    day_of_week = models.JSONField()

    def __str__(self):
        return f"{self.station_name} - {self.rental_date} - {self.rental_hour}시"
