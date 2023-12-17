import folium
import webbrowser
import requests
import pandas as pd
from sqlalchemy import create_engine
from folium import plugins
from django.shortcuts import render
from django.db.utils import IntegrityError
from django.http import HttpResponse
from datetime import datetime
from myapp.models import BikeStation, PredictionBicycle
import os
import time
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

# myapp/views.py

def load_prediction_data():
    df = pd.read_csv("prediction_bicycle.csv", encoding="euc-kr")
    engine = create_engine('postgresql://postgres:john0312@localhost:5432/realtimebike')
    df.to_sql('predictionbike', engine, if_exists='replace', index=False)

def bike_station_predictions(request):
    # 예측 데이터 로딩 및 처리 로직
    # ...
    df = pd.read_csv("prediction_bicycle.csv", encoding="euc-kr")
    for index, row in df.iterrows():
        PredictionBicycle.objects.update_or_create(
            station_name=row['대여소명'],
            rental_date=row['대여일자'],
            rental_hour=row['대여시간'],
            expected_usage=row['예상이용건수'],
            temperature=row['기온(°C)'],
            wind_speed=row['풍속(m/s)'],
            rainfall=row['강수량(mm)'],
            humidity=row['습도(%)'],
            day_of_week=row[['요일_0', '요일_1', '요일_2', '요일_3', '요일_4', '요일_5', '요일_6']].to_dict()
        )
    current_date = datetime.now().strftime('%Y-%m-%d')
    current_hour = datetime.now().hour

    # 부족한 대여소 식별
    shortage_stations = []
    for prediction in PredictionBicycle.objects.filter(rental_date=current_date, rental_hour=current_hour):
        bike_station = BikeStation.objects.get(station_name=prediction.station_name)
        if bike_station.parking_bike_count - prediction.expected_usage < 2:
            shortage_stations.append(bike_station)

    context = {
        'shortage_stations': shortage_stations,
    }
    return render(request, 'bike_predictions.html', context)

