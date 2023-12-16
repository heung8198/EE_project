from django.contrib import admin
from .models import BikeStation

@admin.register(BikeStation)
class BikeStationAdmin(admin.ModelAdmin):
    list_display = ['station_name', 'parking_bike_count', 'total_rack_count', 'latitude', 'longitude']
    # 필요에 따라 다른 옵션을 추가할 수 있습니다.
