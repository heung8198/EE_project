import folium
import webbrowser
import pandas as pd
import os
import time
import requests
import psycopg2
import urllib
import re
import io
import sys
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import warnings
from sqlalchemy import create_engine
from folium import plugins
from django.shortcuts import render
from django.db.utils import IntegrityError
from django.http import HttpResponse
from datetime import datetime
from myapp.models import BikeStation, PredictionBicycle
from datetime import datetime, date, timedelta
from urllib.parse import urlencode
from urllib.parse import quote_plus
from django.conf import settings
from django.db import connection

# 이하 함수 정의들...

def fetch_bike_data(sender=None, **kwargs):
    file_path = os.path.join('templates', 'bike_map.html')

    # 파일이 이미 존재하는 경우 삭제
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Error while deleting the file: {e}")
    # API 호출 및 데이터 처리 코드
    # 예: requests.get('API_URL')...
    # """
    # 서울특별시 공공자전거 실시간 대여정보 API 데이터 가져오기
    # 대여소별 실시간 자전거 대여가능 건수, 거치율, 대여소 위치정보를 제공.
    # 호출시 시스템 부하로 한번에 최대 1,000건를 초과할수 없음.
    # 3회 나누어 호출하는 코드작성 예) 1/1,000, 1001/2,000, 2001/3000 (대여소 수 : 2705개소)
    # """
    try:
        import http.client as http_client
    except ImportError:
        import httplib as http_client
    http_client.HTTPConnection.debuglevel = 0

    apikey = "796158756e6a75393434677248417a"

    startnum = 1
    endnum = 1000
    # URL : http://openapi.seoul.go.kr:8088/{인증키}/json/bikeList/1/5/
    url1 = (
            "http://openapi.seoul.go.kr:8088/" + apikey + f"/json/bikeList/{startnum}/{endnum}/"
    )

    json1 = requests.get(url1).json()
    raw1 = pd.DataFrame(json1["rentBikeStatus"]["row"])

    startnum = 1001
    endnum = 2000
    # URL : http://openapi.seoul.go.kr:8088/{인증키}/json/bikeList/1/5/
    url2 = (
            "http://openapi.seoul.go.kr:8088/" + apikey + f"/json/bikeList/{startnum}/{endnum}/"
    )
    json2 = requests.get(url2).json()
    raw2 = pd.DataFrame(json2["rentBikeStatus"]["row"])

    startnum = 2001
    endnum = 3000
    # URL : http://openapi.seoul.go.kr:8088/{인증키}/json/bikeList/1/5/
    url3 = (
            "http://openapi.seoul.go.kr:8088/" + apikey + f"/json/bikeList/{startnum}/{endnum}/"
    )
    json3 = requests.get(url3).json()
    raw3 = pd.DataFrame(json3["rentBikeStatus"]["row"])

    data = pd.concat([raw1, raw2, raw3])
    data.reset_index(drop=True)
    data.rename(
        columns={
            "rackTotCnt": "거치대개수",
            "stationName": "대여소이름",
            "parkingBikeTotCnt": "주차된 자전거 수",
            "shared": "거치율",
            "stationLatitude": "위도",
            "stationLongitude": "경도",
            "stationId": "대여소ID",
        },
        inplace=True,
    )
    # print(data.info())
    station = [
        "593.자양중앙나들목",
        "592. 건국대학교 학생회관",
        "591. 건국대학교 (행정관)",
        "590. 건국대학교 (입학정보관)",
        "588. 뚝섬 유원지역",
        "584. 광진광장 교통섬",
        "577. 광진청소년수련관",
        "576. 광나루역 3번 출구",
        "575. 대원중고교 입구(대하빌딩)",
        "574. 아차산역4번출구",
        "573. 구의문주차장 앞",
        "571. 세종대학교 대양AI센터",
        "555. 구의3동주민센터",
        "553. 중곡 성원아파트 앞",
        "552. 대림아크로리버 앞",
        "551. 구의삼성쉐르빌 앞",
        "549. 아차산역 3번출구",
        "548. 자양나들목",
        "546. 잠실대교북단 교차로",
        "544. 광남중학교",
        "543. 구의공원(테크노마트 앞)",
        "542. 강변역 4번출구 뒤",
        "540. 군자역 7번출구 베스트샵 앞",
        "539. 군자교교차로",
        "516. 광진메디칼 앞",
        "515. 광양중학교 앞",
        "505. 자양사거리 광진아크로텔 앞",
        "502. 뚝섬유원지역 1번출구 앞",
        "501. 광진구의회 앞",
        "500. 어린이대공원역 3번출구 앞",
        "3886.광진구 민방위교육센터",
        "3882. 자양2동 주민센터",
        "3881. 신자초교입구 교차로",
        "3880. 홍련봉 공원",
        "3879. 중랑천 뚝방길 산책로 입구",
        "3878. 장로회신학대학교 주기철 기념관",
        "3873. 동서울우편집중국 앞",
        "3868. 자양한강도서관",
        "3865. 이튼타워리버 2차",
        "3864. 광진소방서 앞",
        "3863. 동일로58길 입구",
        "3860. 건국대학교 정문 앞",
        "3853. 어린이대공원역 2번출구",
        "3588.세종대학교(영실관)",
        "3587.우성식품 앞",
        "3586.군자역 비채온 오피스텔",
        "3582.화양동 우체국",
        "3581.광진광장",
        "3579.광진 캠퍼스시티",
        "3575. 자양사거리(서원빌딩)",
        "3573.광나루안전체험관",
        "3571.화양 APT(횡단보도 옆)",
        "3570.구의역 리버비스타 오피스텔",
        "3569.건대병원후문",
        "3566.우성4차아파트",
        "3564.나루마당",
        "3563.구의7단지현대아파트",
        "3543. 세종대학교(학술정보원)",
        "3542. 래미안 구의파크 스위트",
        "3541. 커먼그라운드",
        "3537. 아차산 휴먼시아 아파트 옆",
        "3536. 중앙농협(자양동)",
        "3534. 건대입구역 5번출구 뒤",
        "3533. 건대입구역 사거리(롯데백화점)",
        "3529. 어린이대공원정문",
        "3528. 광진정보도서관",
        "3524. 세종대학교",
        "3523. 건국대학교 과학관(이과대) 앞",
        "3521. 현대홈타운 뒷길",
        "3520. 광진경찰서",
        "3518. 군자역 7번출구뒤",
        "3517. 용마사거리",
        "3516. 구의아리수정수센터앞",
        "3510. 중곡SK아파트앞",
        "3509. 세종사이버대학교",
        "3508. 화양사거리",
        "3507. 어린이회관",
        "3506. 영동대교 북단",
        "3505. 신양초교앞 교차로",
        "3504. 원일교회",
        "3503. 광진유진스웰",
        "3502. 중곡역 1번출구",
        "3501. 광진구청 앞",
        "3500. 군자역2번출구",
        "3890. 웰츠타워 오피스텔",
        "3891. 군자역4번출구",
    ]
    data = data[data["대여소이름"].isin(station)]
    data = data[["거치대개수", "대여소이름", "주차된 자전거 수", "거치율", "위도", "경도", "대여소ID"]]
    # 데이터베이스 연결 정보 설정
    user = "postgres"
    password = "john0312"
    host = "localhost"
    port = "5432"
    database = "realtimebike"
    table_name = "realtimebike"
    # 데이터베이스 엔진 생성
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")
    # DataFrame을 PostgreSQL에 저장
    # 데이터베이스에 저장하는 코드를 try-except 블록으로 감싸 오류 처리
    try:
        data.to_sql(table_name, engine, if_exists="replace", index=False)
    except Exception as e:
        print("Error while saving to database:", e)

    query = f"SELECT * FROM {table_name}"
    data = pd.read_sql_query(query, engine)

    # "주차된 자전거 수"와 "거치대개수" 열을 숫자형으로 변환
    data["주차된 자전거 수"] = pd.to_numeric(data["주차된 자전거 수"], errors="coerce")
    data["거치대개수"] = pd.to_numeric(data["거치대개수"], errors="coerce")

    # 결측치를 처리하는 방법 (예: 0으로 채우기)
    data.fillna(0, inplace=True)
    # 데이터베이스에 저장하는 로직
    for index, row in data.iterrows():
        try:
            BikeStation.objects.update_or_create(
                station_name=row['대여소이름'],
                defaults={
                    'parking_bike_count': row['주차된 자전거 수'],
                    'total_rack_count': row['거치대개수'],
                    'latitude': row['위도'],
                    'longitude': row['경도']
                }
            )
        except IntegrityError as e:
            print(f"Error saving data for {row['대여소이름']}: {e}")
    # 지도 생성하기
    m = folium.Map(location=["37.55", "127.085"], zoom_start=14)
    # 마커 추가하기
    for i in range(len(data)):
        name = data.loc[i, "대여소이름"]
        available = data.loc[i, "주차된 자전거 수"]
        total = data.loc[i, "거치대개수"]
        lat = data.loc[i, "위도"]
        long = data.loc[i, "경도"]

        # 자전거 수량에 대해 색상으로 표시
        ##  자전거 보유율이 50% 초과일 경우 --> 파란색
        ##  현재 자전거가 2대 보다 적을 경우 --> 빨간색
        ##  그 외의 경우(자전거 2대 이상 이면서, 자전거 보유율 50% 미만) --> 초록색
        if available / total > 0.5:
            color = "blue"
        elif available < 2:
            color = "red"
        else:
            color = "green"

        folium.Marker(
            location=[lat, long],
            tooltip=f"{name} : {available}",
            icon=plugins.BeautifyIcon(
                icon="arrow-down",
                icon_shape="marker",
                border_color=color,
                number=int(available),
            ),
        ).add_to(m)
    # 지도를 HTML 파일로 저장
    try:
        m.save(file_path)
    except Exception as e:
        print("Error while saving the file:", e)
    # HTML 파일이 업데이트될 시간을 주기 위해 5초간 대기
    time.sleep(5)

def fetch_bike_data_view(request):
    # # HTML 파일이 업데이트될 시간을 주기 위해 5초간 대기
    # time.sleep(5)
    # 여기서 fetch_bike_data 함수를 호출
    fetch_bike_data()
    return HttpResponse("Bike data fetched and updated.")


    # 기존의 bike_stations 함수를 다음과 같이 수정합니다.
def bike_station_shortages(request):
    shortage_stations = BikeStation.objects.filter(parking_bike_count__lt=2)
    context = {
        'shortage_stations': shortage_stations,
    }
    return render(request, 'bike_stations.html', context)

def bike_number_prediction(request):
    one_hour_later = datetime.now() + timedelta(hours=1)
    future_date = one_hour_later.strftime('%Y-%m-%d')
    future_hour = one_hour_later.hour

    # 예측 데이터 가져오기
    with connection.cursor() as cursor:
        query = """
            SELECT station_name, expected_usage
            FROM prediction_bicycle
            WHERE rental_date = %s AND rental_hour = %s;
        """
        cursor.execute(query, [future_date, future_hour])
        predictions = cursor.fetchall()

    station_predictions = []
    for station_name, expected_usage in predictions:
        # 해당 대여소의 현재 상태를 가져온다
        with connection.cursor() as cursor:
            query = """
                SELECT parking_bike_count
                FROM myapp_bikestation
                WHERE station_name = %s;
            """
            cursor.execute(query, [station_name])
            bike_station_info = cursor.fetchone()

        # bike_station_info가 존재하면 계산 수행
        if bike_station_info:
            parking_bike_count = bike_station_info[0]
            prediction_after_hour = parking_bike_count - expected_usage
            print(
                f"Station: {station_name}, Current: {parking_bike_count}, Expected: {expected_usage}, Difference: {prediction_after_hour}")
            if prediction_after_hour < 1:
                station_predictions.append({
                    'station_name': station_name,
                    'current_count': parking_bike_count,
                    'predicted_count': expected_usage,
                    'difference': prediction_after_hour
                })

    # 결과를 템플릿에 전달
    context = {
        'station_predictions': station_predictions
    }
    return render(request, 'bike_stations.html', context)

# myapp/views.py
def fetch_weather_data(request):
    # 여기에 날씨 데이터를 가져오고 처리하는 코드를 작성
    # 예: API 호출, 데이터베이스 저장 등

    # 표준 출력 인코딩 설정
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
    # 표준 에러 인코딩 설정
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
    # 기상청_동네 예보 조회 서비스 api 데이터 url 주소, 초단기이기때문에 getUltraSrtFcst 사용
    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst"

    serviceKey = "L16Ur8uLM4EwFCkfaKj69wuzy8oZaieY%2BtZTecZY2E5J4G%2BEdjNxt42hWC1jFCRkpNxQgbMLAj8K%2FQAIKz3Qcg%3D%3D"  # 공공데이터 포털에서 생성된 본인의 서비스 키를 복사 / 붙여넣기
    serviceKeyDecoded = urllib.parse.unquote(
        serviceKey, "UTF-8"
    )  # 공데이터 포털에서 제공하는 서비스키는 이미 인코딩된 상태이므로, 디코딩하여 사용해야 함

    now = datetime.now()
    today = datetime.today().strftime("%Y%m%d")
    y = date.today() - timedelta(days=1)
    yesterday = y.strftime("%Y%m%d")
    nx = 62  # 광진구 위도와 경도를 x,y좌표로 변경
    ny = 126

    if now.minute < 45:  # base_time와 base_date 구하는 함수
        if now.hour == 0:
            base_time = "2330"
            base_date = yesterday
        else:
            pre_hour = now.hour - 1
            if pre_hour < 10:
                base_time = "0" + str(pre_hour) + "30"
            else:
                base_time = str(pre_hour) + "30"
            base_date = today
    else:
        if now.hour < 10:
            base_time = "0" + str(now.hour) + "30"
        else:
            base_time = str(now.hour) + "30"
        base_date = today

    queryParams = "?" + urlencode(
        {
            quote_plus("serviceKey"): serviceKeyDecoded,
            quote_plus("base_date"): base_date,
            quote_plus("base_time"): base_time,
            quote_plus("nx"): nx,
            quote_plus("ny"): ny,
            quote_plus("dataType"): "json",
            quote_plus("numOfRows"): "60",
            quote_plus("pageNo"): "1",
        }
    )  # 페이지로 안나누고 한번에 받아오기 위해 numOfRows=60으로 설정해주었다

    # 값 요청 (웹 브라우저 서버에서 요청 - url주소와 파라미터)
    res = requests.get(url + queryParams, verify=False)  # verify=False이거 안 넣으면 에러남ㅜㅜ
    items = res.json().get("response").get("body").get("items")  # 데이터들 아이템에 저장

    # 저장할 데이터 항목의 이름을 입력합니다.
    column_names = ["대여일자", "대여시간", "기온(°C)", "풍속(m/s)", "강수량(mm)", "습도(%)"]
    data_rows = []

    # 각 예보 카테고리에 대한 변수를 초기화합니다.
    data_dict = {}

    def add_weekday_columns(df):
        # 요일에 대한 열을 추가
        weekdays = ["요일_0", "요일_1", "요일_2", "요일_3", "요일_4", "요일_5", "요일_6"]
        for weekday in weekdays:
            df[weekday] = 0

        # 각 행의 날짜에 따라 해당 요일 열에 1을 설정
        for index, row in df.iterrows():
            weekday = datetime.strptime(row["대여일자"], "%Y-%m-%d").weekday()
            df.at[index, "요일_" + str(weekday)] = 1

        return df

    # 날짜와 시간 처리를 위한 수정
    # 날짜와 시간 형식을 변경하는 함수
    def format_date_and_time(fcstDate, fcstTime):
        # fcstTime을 'HHMM' 형식에서 'HH' 형식으로 변경
        fcstTimeFormatted = fcstTime[:2]
        fcst_datetime = datetime.strptime(fcstDate + fcstTimeFormatted, "%Y%m%d%H")
        return fcst_datetime.strftime("%Y-%m-%d"), fcst_datetime.strftime("%H")

    # 'category' 값이 T1H, RN1, WSD, REH인 경우에 대해 처리합니다.
    for item in items["item"]:
        # 해당 'category'에 따라 데이터를 저장합니다.
        if item["category"] in ["T1H", "WSD", "RN1", "REH"]:
            if item["fcstTime"] not in data_dict:
                data_dict[item["fcstTime"]] = {}
                # 날짜와 시간 형식 변경
                formatted_date, formatted_time = format_date_and_time(item["fcstDate"], item["fcstTime"])
            if item["category"] == "T1H":
                data_dict[item["fcstTime"]]["기온(°C)"] = int(item["fcstValue"])
            elif item["category"] == "WSD":
                data_dict[item["fcstTime"]]["풍속(m/s)"] = int(item["fcstValue"])
            elif item["category"] == "RN1":
                # 정확한 형식에 맞게 정규 표현식 수정
                numeric_value = re.findall("\d+\.\d+|\d+", item["fcstValue"])
                if numeric_value:
                    # 리스트의 첫 번째 값(소수점 포함 숫자)을 float로 변환하여 저장
                    data_dict[item["fcstTime"]]["강수량(mm)"] = float(numeric_value[0])
                else:
                    # 예외 처리: 추출된 값이 없거나 예상과 다른 경우 0.0 사용
                    data_dict[item["fcstTime"]]["강수량(mm)"] = 0.0

            elif item["category"] == "REH":
                data_dict[item["fcstTime"]]["습도(%)"] = int(item["fcstValue"])

    # 1시간 단위로 6시간동안 각 예보 값을 저장합니다.
    for fcstTime, data in data_dict.items():
        formatted_date, formatted_time = format_date_and_time(item["fcstDate"], fcstTime + "00")
        data_rows.append(
            [
                formatted_date,
                formatted_time,
                data.get("기온(°C)"),
                data.get("풍속(m/s)"),
                data.get("강수량(mm)"),
                data.get("습도(%)"),
            ]
        )

    user = "postgres"
    password = "john0312"
    host = "localhost"
    port = "5432"
    database = "realtimebike"
    table_name = "predictionweather"
    # 데이터베이스 엔진 생성
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")
    # DataFrame을 PostgreSQL에 저장
    # 데이터베이스에 저장하는 코드를 try-except 블록으로 감싸 오류 처리
    weather_data = pd.DataFrame(data_rows, columns=column_names)

    # 요일 열 추가
    weather_data = add_weekday_columns(weather_data)
    try:
        weather_data.to_sql(table_name, engine, if_exists="replace", index=False)
    except Exception as e:
        print("Error while saving to database:", e)

    # 처리가 완료된 후 사용자에게 메시지를 반환
    return HttpResponse("날씨 데이터가 성공적으로 업데이트되었습니다.")

def fetch_learning_data(request):

    #먼저 postgresql db에 해당하는 엔진을 만들기 위한 여러가지 선언
    user = "postgres"
    password = "john0312"
    host = "localhost"
    port = "5432"
    database = "realtimebike"
    tablename= "prediction_bicycle"

    bike_table="pastbike"
    weather_table="predictionweather"
    # 데이터베이스 엔진 생성
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")
    # DataFrame을 PostgreSQL에 저장


    warnings.filterwarnings("ignore")

    mpl.rcParams["axes.unicode_minus"] = False
    plt.rcParams["font.family"] = "Malgun Gothic"  # 기존에 'NanumGothic'

    df = pd.read_sql_query(f"SELECT * FROM {bike_table}", engine)
    df["대여시간"] = pd.to_numeric(df["대여시간"], errors='coerce')

    df["대여소명"] = df["대여소명"].astype("category")
    df["대여소명"] = df["대여소명"].cat.remove_unused_categories()

    stations = [
        "593.자양중앙나들목",
        "592. 건국대학교 학생회관",
        "591. 건국대학교 (행정관)",
        "590. 건국대학교 (입학정보관)",
        "588. 뚝섬 유원지역",
        "584. 광진광장 교통섬",
        "577. 광진청소년수련관",
        "576. 광나루역 3번 출구",
        "575. 대원중고교 입구(대하빌딩)",
        "574. 아차산역4번출구",
        "573. 구의문주차장 앞",
        "571. 세종대학교 대양AI센터",
        "555. 구의3동주민센터",
        "553. 중곡 성원아파트 앞",
        "552. 대림아크로리버 앞",
        "551. 구의삼성쉐르빌 앞",
        "549. 아차산역 3번출구",
        "548. 자양나들목",
        "546. 잠실대교북단 교차로",
        "544. 광남중학교",
        "543. 구의공원(테크노마트 앞)",
        "542. 강변역 4번출구 뒤",
        "540. 군자역 7번출구 베스트샵 앞",
        "539. 군자교교차로",
        "516. 광진메디칼 앞",
        "515. 광양중학교 앞",
        "505. 자양사거리 광진아크로텔 앞",
        "502. 뚝섬유원지역 1번출구 앞",
        "501. 광진구의회 앞",
        "500. 어린이대공원역 3번출구 앞",
        "3886.광진구 민방위교육센터",
        "3882. 자양2동 주민센터",
        "3881. 신자초교입구 교차로",
        "3880. 홍련봉 공원",
        "3879. 중랑천 뚝방길 산책로 입구",
        "3878. 장로회신학대학교 주기철 기념관",
        "3873. 동서울우편집중국 앞",
        "3868. 자양한강도서관",
        "3865. 이튼타워리버 2차",
        "3864. 광진소방서 앞",
        "3863. 동일로58길 입구",
        "3860. 건국대학교 정문 앞",
        "3853. 어린이대공원역 2번출구",
        "3588.세종대학교(영실관)",
        "3587.우성식품 앞",
        "3586.군자역 비채온 오피스텔",
        "3582.화양동 우체국",
        "3581.광진광장",
        "3579.광진 캠퍼스시티",
        "3575. 자양사거리(서원빌딩)",
        "3573.광나루안전체험관",
        "3571.화양 APT(횡단보도 옆)",
        "3570.구의역 리버비스타 오피스텔",
        "3569.건대병원후문",
        "3566.우성4차아파트",
        "3564.나루마당",
        "3563.구의7단지현대아파트",
        "3543. 세종대학교(학술정보원)",
        "3542. 래미안 구의파크 스위트",
        "3541. 커먼그라운드",
        "3537. 아차산 휴먼시아 아파트 옆",
        "3536. 중앙농협(자양동)",
        "3534. 건대입구역 5번출구 뒤",
        "3533. 건대입구역 사거리(롯데백화점)",
        "3529. 어린이대공원정문",
        "3528. 광진정보도서관",
        "3524. 세종대학교",
        "3523. 건국대학교 과학관(이과대) 앞",
        "3521. 현대홈타운 뒷길",
        "3520. 광진경찰서",
        "3518. 군자역 7번출구뒤",
        "3517. 용마사거리",
        "3516. 구의아리수정수센터앞",
        "3510. 중곡SK아파트앞",
        "3509. 세종사이버대학교",
        "3508. 화양사거리",
        "3507. 어린이회관",
        "3506. 영동대교 북단",
        "3505. 신양초교앞 교차로",
        "3504. 원일교회",
        "3503. 광진유진스웰",
        "3502. 중곡역 1번출구",
        "3501. 광진구청 앞",
        "3500. 군자역2번출구",
        "3890. 웰츠타워 오피스텔",
        "3891. 군자역4번출구"
    ]

    prediction_bicycle = pd.DataFrame()  # 예측 값 넣을 빈 데이터프레임 생성

    # 모든 정류장에 대해서 xgboost로 예측
    for st in stations: #모든 정류장을 반복문으로 실행
        specific = df[df["대여소명"] == st]

        specific = specific.join(pd.get_dummies(specific["요일"], prefix="요일"))

        dayofweek = ["요일_" + str(i) for i in range(7)]
        features = ["대여시간", "기온(°C)", "풍속(m/s)", "강수량(mm)", "습도(%)"] + dayofweek
        specific = specific.replace({True: 1, False: 0})

        from sklearn.model_selection import train_test_split

        X_train, X_test, y_train, y_test = train_test_split(
            specific[features], specific["이용건수"], test_size=0.2, random_state=42
        )#train 데이터와 test 데이터를 나누기

        print(X_train.shape)
        print(X_test.shape)

        from sklearn.metrics import mean_absolute_error
        from sklearn.model_selection import GridSearchCV
        #from sklearn import linear_model as lm   *linear model
        import xgboost as xgb
        from scipy.stats import uniform, randint
        from sklearn.metrics import mean_squared_error

        model = ("xgboost", xgb.XGBRegressor())

        # 하이퍼 파라미터 튜닝을 위한 params
        n = 3

        params = {
            "xgboost": {
                "gamma": uniform(0, 0.5).rvs(n),
                "max_depth": range(2, 7),  # default 3
                "n_estimators": randint(100, 150).rvs(n),  # default 100
            }

        }

        trained_model = xgb.XGBRegressor(enable_categorical=True).fit(X_train, y_train) # train 데이터를 바탕으로 train된 모델 생성

        predictions = trained_model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        rmse = np.sqrt(mse) #X_test 데이터에 대해서 예측하고 성능 검증하기 위해서 rmse사용

        weather_prediction = pd.read_sql_query(f"SELECT * FROM {weather_table}", engine) # db에서 예측된 날씨데이터 가져오기
        weather_prediction["대여시간"] = pd.to_numeric(weather_prediction["대여시간"], errors='coerce')
        api_data = weather_prediction.drop('대여일자',axis=1)# 예측하기 위해서 예측 데이터 형식과 맞게 대여일자를 drop

        predictions = trained_model.predict(api_data)
        predictions = [0 if x < 0 else round(x) if not x.is_integer() else x for x in predictions]  # 음수 값을 0으로 변경

        weather_prediction.insert(2, '예상이용건수', predictions)
        weather_prediction.insert(0, '대여소명', st) # 원래 있던 데이터 형식과 맞추기 위해서 columns 삽입

        weather_prediction["예상이용건수"] = weather_prediction["예상이용건수"].astype("int32")#예측된 값 형식 int 형으로 바꾸기
        weather_prediction["대여일자"] = weather_prediction["대여일자"].astype("datetime64[ns]")
        weather_prediction["대여시간"] = weather_prediction["대여시간"].astype("int32")
        weather_prediction["대여소명"] = weather_prediction["대여소명"].astype("category")
        weather_prediction["기온(°C)"] = weather_prediction["기온(°C)"].astype("int32")
        weather_prediction["풍속(m/s)"] = weather_prediction["풍속(m/s)"].astype("int32")
        weather_prediction["강수량(mm)"] = weather_prediction["강수량(mm)"].astype("int32")
        weather_prediction["습도(%)"] = weather_prediction["습도(%)"].astype("int32")

        weather_prediction.rename(columns={'예상이용건수': 'expected_usage', '대여일자': 'rental_date',
                                           '대여시간': 'rental_hour','대여소명':'station_name'}, inplace=True)

        prediction_bicycle = pd.concat([prediction_bicycle, weather_prediction])#예측된 값들 합쳐서 하나의 데이터프레임 만들기
        # prediction_bicycle.to_csv('prediction_bicycle.csv',index=False,encoding = 'cp949')
    try:
        prediction_bicycle.to_sql(tablename, engine, if_exists="replace", index=False)
    except Exception as e:
        print("Error while saving to database:", e)

    # return 0
        # 처리가 완료된 후 사용자에게 메시지를 반환
    return HttpResponse("22년 자전거 학습 데이터가 성공적으로 업데이트되었습니다.")
