# myapp/apps.py
from django.apps import AppConfig
from django.db.models.signals import post_migrate

class MyappConfig(AppConfig):
    name = 'myapp'

    def ready(self):
        from myapp.views import fetch_bike_data, fetch_learning_data
        # 서버 시작 시 fetch_bike_data 함수 호출
        fetch_bike_data()
        post_migrate.connect(fetch_bike_data, sender=self)
        # fetch_learning_data(request)
        # post_migrate.connect(fetch_learning_data, sender=self)
        # 함수 호출
        # save_data()
        # post_migrate.connect(save_data, sender=self)
