from django.db import models

class BikeStation(models.Model):
    station_name = models.CharField(max_length=100)
    parking_bike_count = models.IntegerField()
    total_rack_count = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    # 기타 필요한 필드 추가

class PredictionBicycle(models.Model):
    id = models.BigAutoField(primary_key=True)
    station_name = models.CharField(max_length=100)
    rental_date = models.CharField()
    rental_hour = models.IntegerField()
    expected_usage = models.IntegerField()
    temperature = models.IntegerField()
    wind_speed = models.IntegerField()
    rainfall = models.FloatField()
    humidity = models.IntegerField()
    day_of_week = models.JSONField()

    class Meta:
        db_table = 'prediction_bicycle'

    # temp_field = models.IntegerField()

    def __str__(self):
        return f"{self.station_name} - {self.rental_date} - {self.rental_hour}시"
