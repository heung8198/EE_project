import os
import sys
import time
import pandas as pd
import numpy as np
import datetime as datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import params as pa

pd.set_option('display.width', 5000)
pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_columns', 5000)

def driversetting(DownloadPath):

    # Selenium Setting
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs",
                                    {"download.default_directory": DownloadPath,
                                     "download.prompt_for_download": False,
                                     "download.directory_upgrade": True,
                                     "safebrowsing_for_trusted_sources_enabled": False,
                                     "safebrowsing.enabled": False})

    #options.add_argument('headless')  # If you want to hide it, show it.
    #options.add_argument('--no-sandbox')
    #options.add_argument('--disable-dev-shm-usage')
    #options.add_argument("start-maximized")

    service = Service()
    driver = webdriver.Chrome(service=service, options=options)

    return driver

def GetGenData(startday,endday):

    driver = driversetting(pa.DownloadPath)

    driver.get(pa.weather)

    print('run website')
    time.sleep(pa.waitseconds)

    # click login
    driver.find_element(By.XPATH, '//*[@id="loginBtn"]').click()
    time.sleep(pa.waitseconds)

    # login
    driver.find_element(By.XPATH, '//*[@id="loginId"]').send_keys(pa.id)
    driver.find_element(By.XPATH, '//*[@id="passwordNo"]').send_keys(pa.password)

    driver.find_element(By.XPATH, '//*[@id="loginbtn"]').click()
    time.sleep(pa.waitseconds)
    print('login')

    driver.find_element(By.XPATH,'//*[@id="gnb"]/div/ul/li[2]/a[1]').click()
    time.sleep(pa.waitseconds)

    #select seoul
    driver.find_element(By.XPATH,'//*[@id="ztree_63_check"]').click()
    time.sleep(pa.waitseconds)

    #select temp
    driver.find_element(By.XPATH,'//*[@id="ztree1_12_check"]').click()

    #select 강수량
    driver.find_element(By.XPATH, '//*[@id="ztree1_15_check"]').click()

    #select humidity
    driver.find_element(By.XPATH, '//*[@id="ztree1_18_check"]').click()

    #select
    driver.find_element(By.XPATH, '//*[@id="ztree1_23_check"]').click()
    time.sleep(pa.waitseconds)

    print('target setting')

    #choose startday
    driver.find_element(By.XPATH,'//*[@id="startDt_d"]').clear()
    driver.find_element(By.XPATH, '//*[@id="startDt_d"]').send_keys(startday)

    #choose endday
    driver.find_element(By.XPATH, '//*[@id="endDt_d"]').clear()
    driver.find_element(By.XPATH, '//*[@id="endDt_d"]').send_keys(endday)

    print('targetday setting')

    #find
    driver.find_element(By.XPATH, '//*[@id="dsForm"]/div[3]/button').click()
    time.sleep(pa.waitseconds)

    #download
    driver.find_element(By.XPATH, '//*[@id="wrap_content"]/div[4]/div[1]/div/a[1]').click()
    time.sleep(pa.waitseconds)


    driver.find_element(By.XPATH,'//*[@id="requestForm"]/ul/li[8]/label').click()
    driver.find_element(By.XPATH,'//*[@id="wrap-datapop"]/div/div[2]/div/a[2]').click()
    print('Download complete')

    time.sleep(pa.waitseconds_download)

    driver.close()

    return []


if __name__ == '__main__':

    startday = '20220101'
    endday = '20221231'

    GetGenData(startday,endday)

    print('1')
