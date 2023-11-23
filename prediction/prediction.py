import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import warnings

warnings.filterwarnings("ignore")

mpl.rcParams["axes.unicode_minus"] = False
plt.rcParams["font.family"] = "NanumGothic"

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

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    ttukseom[features], ttukseom["이용건수"], test_size=0.2, random_state=42
)
print(X_train.shape)
print(X_test.shape)

from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import GridSearchCV
from sklearn import linear_model as lm
import xgboost as xgb
from scipy.stats import uniform, randint

models = [
     ("lr", lm.LinearRegression(n_jobs=-1)),
     ("ridge", lm.Ridge()),
     ("lasso", lm.Lasso()),
     ("elastic", lm.ElasticNet()),
     ("LassoLars", lm.LassoLars(max_iter=100)),
     ("LogisticRegression", lm.LogisticRegression(max_iter=5000)),
     ("SGDRegressor", lm.SGDRegressor()),
     ("Perceptron", lm.Perceptron(n_jobs=-1)),
    ("xgboost", xgb.XGBRegressor()),
]
n = 3
params = {
    "lr": {
        "fit_intercept": [True, False],
        #"normalize": [True, False],
    },
    "ridge": {
        "alpha": [0.01, 0.1, 1.0, 10, 100],
        "fit_intercept": [True, False],
        #"normalize": [True, False],
    },
    "lasso": {
        "alpha": [0.1, 1.0, 10],
        "fit_intercept": [True, False],
        #"normalize": [True, False],
    },
    "elastic": {
        "alpha": [0.1, 1.0, 10],
        #"normalize": [True, False],
        "fit_intercept": [True, False],
    },
    "LassoLars": {
        "alpha": [0.1, 1.0, 10],
        #"normalize": [True, False],
        "fit_intercept": [True, False],
    },
    "LogisticRegression": {
        "penalty": ["l1", "l2"],
        "C": [0.001, 0.01, 0.1, 1.0, 10, 100],
        "fit_intercept": [True, False],
    },
    "SGDRegressor": {
        "penalty": ["l1", "l2"],
        "alpha": [0.001, 0.01, 0.1, 1.0, 10, 100],
        "fit_intercept": [True, False],
    },
    "Perceptron": {
        "penalty": ["None", "l1", "l2"],
        "alpha": [0.001, 0.01, 0.1, 1.0, 10, 100],
        "fit_intercept": [True, False],
    },
    "xgboost": {
        "gamma": uniform(0, 0.5).rvs(n),
        "max_depth": range(2, 7),  # default 3
        "n_estimators": randint(100, 150).rvs(n),  # default 100
    },
}

best_model, best_mae = None, float("inf")
for model_name, model in models:
    param_grid = params[model_name]
    grid = GridSearchCV(model, cv=5, n_jobs=-1, param_grid=param_grid)
    grid = grid.fit(X_train, y_train)

    model = grid.best_estimator_
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)

    print(model_name, mae)

    if mae < best_mae:
        best_model = model

# XGBRegressor(
#     base_score=0.5,
#     booster="gbtree",
#     colsample_bylevel=1,
#     colsample_bytree=1,
#     gamma=0.35336819357599547,
#     importance_type="gain",
#     learning_rate=0.1,
#     max_delta_step=0,
#     max_depth=6,
#     min_child_weight=1,
#     missing=None,
#     n_estimators=102,
#     n_jobs=1,
#     nthread=None,
#     objective="reg:linear",
#     random_state=0,
#     reg_alpha=0,
#     reg_lambda=1,
#     scale_pos_weight=1,
#     seed=None,
#     silent=True,
#     subsample=1,
# )
feature_importance = pd.Series(
    index=features, data=best_model.feature_importances_
).sort_values(ascending=False)
feature_importance.plot(kind="bar", figsize=(24, 5), title="피쳐 중요도", rot=0)
plt.show()

predictions = best_model.predict(X_test)

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