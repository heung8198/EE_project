from django.contrib import admin
from .models import BikeStation, PredictionBicycle

@admin.register(BikeStation)
class BikeStationAdmin(admin.ModelAdmin):
    list_display = ['station_name', 'parking_bike_count', 'total_rack_count', 'latitude', 'longitude']
    # 필요에 따라 다른 옵션을 추가할 수 있습니다.



@admin.register(PredictionBicycle)
class PredictionBicycleAdmin(admin.ModelAdmin):
    list_display = ['station_name', 'rental_date', 'rental_hour', 'expected_usage', 'temperature', 'wind_speed', 'rainfall', 'humidity', 'day_of_week']

    # def formatted_rental_date(self, obj):
    #     return obj.rental_date.strftime('%Y-%m-%d')
    # formatted_rental_date.short_description = 'Rental Date'
    # PredictionBicycle.objects.filter(day_of_week__요일_6=1)
