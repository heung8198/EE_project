import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import warnings

warnings.filterwarnings("ignore")

mpl.rcParams["axes.unicode_minus"] = False
plt.rcParams["font.family"] = "Malgun Gothic" # 기존에 'NanumGothic'

df = pd.read_csv(
    r"C:\Users\gmdwh\Documents\midterm_project\bike.csv",
    encoding="cp949",
)

print(df.columns)

df["대여소명"] = df["대여소명"].astype("category")
df["대여소명"] = df["대여소명"].cat.remove_unused_categories()

ttukseom = df[df["대여소명"] == "502. 뚝섬유원지역 1번출구 앞"] # 뚟섬 정류장 하나만 일단 시행

print(ttukseom.head())
ttukseom = ttukseom.join(pd.get_dummies(ttukseom["요일"], prefix="요일"))

dayofweek = ["요일_" + str(i) for i in range(7)]
features = ["월", "대여시간", "기온(°C)", "풍속(m/s)", "강수량(mm)", "습도(%)"] + dayofweek
ttukseom = ttukseom.replace({True: 1, False: 0})
print(ttukseom.head())

ttukseom.to_csv(
        r"C:\Users\gmdwh\Documents\midterm_project\ttukseom.csv",
        index=False,
        encoding="euc-kr")

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    ttukseom[features], ttukseom["이용건수"], test_size=0.2, random_state=42
)
print(X_train.shape)
print(X_test.shape)

from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import GridSearchCV
#from sklearn import linear_model as lm   *linear model
import xgboost as xgb
from scipy.stats import uniform, randint

models = [("xgboost", xgb.XGBRegressor())]

n = 3

params={
    "xgboost": {
            "gamma": uniform(0, 0.5).rvs(n),
            "max_depth": range(2, 7),  # default 3
            "n_estimators": randint(100, 150).rvs(n),  # default 100
        }

}


grid = xgb.XGBRegressor().fit(X_train, y_train)

predictions = grid.predict(X_test)
mae = mean_absolute_error(y_test, predictions)

feature_importance = pd.Series(
    index=features, data=grid.feature_importances_
).sort_values(ascending=False)
feature_importance.plot(kind="bar", figsize=(24, 5), title="피쳐 중요도", rot=0)
plt.show()

fig, axes = plt.subplots(1, 2, figsize=(25, 5))
sns.distplot(predictions, ax=axes[0])
axes[0].set_title("예측 값 분포")
sns.distplot(y_test, ax=axes[1])
axes[1].set_title("실제 값 분포")
plt.show()


plt.figure(figsize=(25, 5))
sns.distplot(abs(predictions - y_test))
plt.title("오차값(절대값) 분포")
plt.show()

print(predictions)