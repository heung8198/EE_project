import requests
from datetime import datetime, date, timedelta
import urllib
from urllib.parse import urlencode
from urllib.parse import quote_plus
import pandas as pd
import numpy
import seaborn

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
    }
)  # 페이지로 안나누고 한번에 받아오기 위해 numOfRows=60으로 설정해주었다


# 값 요청 (웹 브라우저 서버에서 요청 - url주소와 파라미터)
res = requests.get(url + queryParams, verify=False)  # verify=False이거 안 넣으면 에러남ㅜㅜ
items = res.json().get("response").get("body").get("items")  # 데이터들 아이템에 저장
# print(items)# 테스트

weather_data = dict()

for item in items["item"]:
    # 기온
    if item["category"] == "T1H":
        weather_data["기온"] = item["fcstValue"]
    # 1시간 동안 강수량
    if item["category"] == "RN1":
        weather_data["강수량"] = item["fcstValue"]
        if weather_data["강수량"] == "강수없음":
            weather_data["강수량"] = 0
    # 풍속
    if item["category"] == "WSD":
        weather_data["풍속"] = item["fcstValue"]
    # 습도
    if item["category"] == "REH":
        weather_data["습도"] = item["fcstValue"]


print("response: ", weather_data)
# columns_name = ["기온", "강수량", "풍속", "습도"]
# weather_df = pd.DataFrame(data=weather_data, index=base_date)
# print(weather_df)
