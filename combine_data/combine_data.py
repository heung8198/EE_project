import pandas as pd
import numpy as np

from datetime import datetime, timedelta

def combine(weather_path):
    df = pd.read_csv(weather_path, encoding="cp949", low_memory=False)

    df.fillna(0, inplace=True)

    df["일시"] = df["일시"].astype("datetime64[ns]")
    df["월"] = df["일시"].dt.month
    df["일"] = df["일시"].dt.day
    df["대여시간"] = df["일시"].dt.hour


    bike = pd.read_csv(
        r"C:\Users\gmdwh\Documents\EE_project\22년_날짜별이용건수_gwangjin.csv",
        encoding="utf-8",
        low_memory=False,
    )

    bike["대여일자"] = bike["대여일자"].astype("datetime64[ns]")
    bike["대여시간"] = bike["대여시간"].astype("int32")
    bike["대여소번호"] = bike["대여소번호"].astype("category")
    bike["대여소명"] = bike["대여소명"].astype("category")
    bike["이용건수"] = bike["이용건수"].astype("int32")


    bike["월"] = bike["대여일자"].dt.month
    bike["일"] = bike["대여일자"].dt.day
    bike["요일"] = bike["대여일자"].dt.dayofweek


    bike = bike.merge(df, on=["월", "일", "대여시간"])
    bike.drop(bike[(bike["대여시간"] > 1) & (bike["대여시간"] < 7)].index, inplace=True)

    bike.to_csv(
        r"C:\Users\gmdwh\Documents\EE_project\bike.csv",
        index=False,
        encoding="euc-kr")

    return bike