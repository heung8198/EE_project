import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import warnings

warnings.filterwarnings("ignore")

mpl.rcParams["axes.unicode_minus"] = False
plt.rcParams["font.family"] = "Malgun Gothic" # 기존에 'NanumGothic'

# csv 파일 불러오기
df = pd.read_csv(
    r"bike.csv",
    encoding="cp949",
)

print(df.columns)

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

prediction_bicycle = pd.DataFrame()

for st in stations:
    specific = df[df["대여소명"] == st] # 뚝섬 정류장 하나만 일단 시행

    print(specific.head())
    specific = specific.join(pd.get_dummies(specific["요일"], prefix="요일"))

    dayofweek = ["요일_" + str(i) for i in range(7)]
    features = ["대여시간", "기온(°C)", "풍속(m/s)", "강수량(mm)", "습도(%)"] + dayofweek
    specific = specific.replace({True: 1, False: 0})
    print(specific.head())

    specific.to_csv(
            r"ttukseom.csv",
            index=False,
            encoding="euc-kr")

    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(
        specific[features], specific["이용건수"], test_size=0.2, random_state=42
    )

    print(X_train.shape)
    print(X_test.shape)

    from sklearn.metrics import mean_absolute_error
    from sklearn.model_selection import GridSearchCV
    #from sklearn import linear_model as lm   *linear model
    import xgboost as xgb
    from scipy.stats import uniform, randint
    from sklearn.metrics import mean_squared_error

    model = ("xgboost", xgb.XGBRegressor())

    n = 3

    params={
        "xgboost": {
                "gamma": uniform(0, 0.5).rvs(n),
                "max_depth": range(2, 7),  # default 3
                "n_estimators": randint(100, 150).rvs(n),  # default 100
            }

    }

    trained_model = xgb.XGBRegressor().fit(X_train, y_train)

    predictions = trained_model.predict(X_test)
    mse=mean_squared_error(y_test, predictions)
    rmse=np.sqrt(mse)


    # 실제 값과 예측 값을 비교하는 산점도 그래프 생성
    # plt.figure(figsize=(10, 6))
    # sns.scatterplot(x=y_test, y=predictions)
    # plt.xlabel('실제 이용건수')
    # plt.ylabel('예측 이용건수')
    # plt.title('실제 이용건수와 예측 이용건수의 비교')
    # plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--') # 대각선 추가
    # plt.show()


    weather_prediction = pd.read_csv(
        r"날씨예보_6시간.csv",
            encoding="utf-8"
    )

    api_data = weather_prediction.drop('대여일자',axis=1)

    predictions = trained_model.predict(api_data)
    predictions = predictions.round(0)

    weather_prediction.insert(2, '예상이용건수', predictions)
    weather_prediction.insert(0,'대여소명',st)

    weather_prediction["예상이용건수"] = weather_prediction["예상이용건수"].astype("int32")

    prediction_bicycle=pd.concat([prediction_bicycle,weather_prediction])

    prediction_bicycle.to_csv(
        r"prediction_bicycle.csv",
        index=False,
        encoding="euc-kr")

# print(data)