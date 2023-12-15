import requests
from datetime import datetime, date, timedelta
import urllib
from urllib.parse import urlencode
from urllib.parse import quote_plus
import pandas as pd
import re

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
column_names = ["대여일자", "대여시간", "기온(°C)", "강수량(mm)", "풍속(m/s)", "습도(%)"]
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
    if item["category"] in ["T1H", "RN1", "WSD", "REH"]:
        if item["fcstTime"] not in data_dict:
            data_dict[item["fcstTime"]] = {}
            # 날짜와 시간 형식 변경
            formatted_date, formatted_time = format_date_and_time(item["fcstDate"], item["fcstTime"])
        if item["category"] == "T1H":
            data_dict[item["fcstTime"]]["기온(°C)"] = int(item["fcstValue"])
        elif item["category"] == "RN1":
                # 정확한 형식에 맞게 정규 표현식 수정
            numeric_value = re.findall("\d+\.\d+|\d+", item["fcstValue"])
            if numeric_value:
                # 리스트의 첫 번째 값(소수점 포함 숫자)을 float로 변환하여 저장
                data_dict[item["fcstTime"]]["강수량(mm)"] = float(numeric_value[0])
            else:
                # 예외 처리: 추출된 값이 없거나 예상과 다른 경우 0.0 사용
                data_dict[item["fcstTime"]]["강수량(mm)"] = 0.0
        elif item["category"] == "WSD":
            data_dict[item["fcstTime"]]["풍속(m/s)"] = int(item["fcstValue"])
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
            data.get("강수량(mm)"),
            data.get("풍속(m/s)"),
            data.get("습도(%)"),
        ]
    )

# 시간대별로 데이터를 불러와서 저장
# 데이터 프레임 생성
weather_data = pd.DataFrame(data_rows, columns=column_names)

# 요일 열 추가
weather_data = add_weekday_columns(weather_data)
# csv 파일로 데이터를 저장합니다.
filename = "C:/Users/user/Documents/EE_project/날씨예보_6시간.csv"
weather_data.to_csv(filename, index=False, encoding="utf-8-sig")

print(f"{filename} 파일이 저장되었습니다.")
