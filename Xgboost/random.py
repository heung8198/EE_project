import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

#matplotlib_inline : pycharm 에서는 필요없음

# 그래프에서 격자로 숫자 범위가 눈에 잘 띄도록 ggplot 스타일을 사용
plt.style.use('ggplot')
# 그래프에서 마이너스 폰트 깨지는 문제에 대한 대처


df = pd.read_csv(r"C:\Users\user\Documents\EE_project\ttukseom.csv",encoding='cp949')


# P~V열 지우기
df = df.drop(columns=['요일_0', '요일_1', '요일_2', '요일_3', '요일_4', '요일_5', '요일_6'])

# 대여시간 열의 값에 ":00:00" 추가
df['대여일자'] = df['일시']

# 원래의 '대여일자'와 '대여시간' 열 삭제
df = df.drop(['일시'], axis=1)
df.to_csv('train.csv', index=False,encoding="euc-kr")

train = pd.read_csv(r"C:\Users\user\Documents\EE_project\Xgboost\train.csv", parse_dates=["대여일자"],encoding='cp949')
print(train.shape)
train.info()

# 엑셀 파일 읽어오기
# CSV 파일 읽어오기
df = pd.read_csv(r"C:\Users\user\Documents\EE_project\날씨예보_6시간.csv", encoding='utf-8')

# 대여일자 및 대여시간 열 조합하여 날짜와 시간으로 표현
df['대여일자'] = pd.to_datetime(df['대여일자'], format='%Y%m%d').dt.strftime('%Y-%m-%d')
df['대여일자'] = df['대여일자'].astype(str) + ' ' + df['대여시간'].astype(str)


# 대여시간 열 삭제
df.drop('대여시간', axis=1, inplace=True)

# 수정된 내용을 새로운 CSV 파일로 저장
df.to_csv('test.csv', index=False, encoding='euc-kr')



test = pd.read_csv(r"C:\Users\user\Documents\EE_project\Xgboost\test.csv",encoding='cp949')
train = pd.read_csv(r"C:\Users\user\Documents\EE_project\Xgboost\train.csv",encoding='cp949')


categorical_feature_names = ['요일']

for var in categorical_feature_names:
    train[var] = train[var].astype("category")
    test[var] = test[var].astype("category")
feature_names = ["대여일자","강수량(mm)", "기온(°C)", "습도(%)", "풍속(m/s)", "요일"]

print(feature_names)

X_train = train[feature_names]

print(X_train.shape)
print(X_train.head())

X_test = test[feature_names]

print(X_test.shape)
print(X_test.head())

label_name = "이용건수"

y_train = train[label_name]

print(y_train.shape)
print(y_train.head())

from sklearn.metrics import make_scorer


def rmsle(predicted_values, actual_values):
    # 넘파이로 배열 형태로 바꿔준다.
    predicted_values = np.array(predicted_values)
    actual_values = np.array(actual_values)

    # 예측값과 실제 값에 1을 더하고 로그를 씌워준다.
    log_predict = np.log(predicted_values + 1)
    log_actual = np.log(actual_values + 1)

    # 위에서 계산한 예측값에서 실제값을 빼주고 제곱을 해준다.
    difference = log_predict - log_actual
    # difference = (log_predict - log_actual) ** 2
    difference = np.square(difference)

    # 평균을 낸다.
    mean_difference = difference.mean()

    # 다시 루트를 씌운다.
    score = np.sqrt(mean_difference)

    return score


rmsle_scorer = make_scorer(rmsle)
print(rmsle_scorer)

from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score

k_fold = KFold(n_splits=10, shuffle=True, random_state=0)
from sklearn.ensemble import RandomForestRegressor

max_depth_list = []

model = RandomForestRegressor(n_estimators=50,
                              n_jobs=-1,
                              random_state=0)
print(model)
#
# score = cross_val_score(model, X_train, y_train, cv=k_fold, scoring=rmsle_scorer)
# score = score.mean()
#


