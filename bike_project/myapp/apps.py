# myapp/apps.py
from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules

class MyappConfig(AppConfig):
    name = 'myapp'

    def ready(self):
        from . import views  # 'tasks.py' 파일에서 함수를 가져옴
        views.fetch_bike_data()  # 함수를 호출