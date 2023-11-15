import params as pa
from project_crawling import project_crawling as cr
from combine_data import combine_data as cb
import os


def file_remove():
    file2 = os.listdir(pa.DownloadPath)
    for f2 in file2:
        if f2.startswith('OBS'):
            FileName = os.path.join(pa.DownloadPath, f2)
            os.remove(FileName)
    return []


def genfile():
    file = os.listdir(pa.DownloadPath)
    for f in file:
        if f.startswith('OBS'):
            weather = os.path.join(pa.DownloadPath, f)

    return weather



if __name__ == '__main__':

    file_remove()
    startday = '20220101'
    endday = '20221231'

    file3 = os.listdir(r"C:\Users\gmdwh\Documents\midterm_project")
    for f in file3:
        if f.startswith('bike'):
            file_name = os.path.join(r"C:\Users\gmdwh\Documents\midterm_project", f)
            os.remove(file_name)

    cr.GetGenData(startday, endday)

    weather_file = genfile()

    data = cb.combine(weather_file)

    file_remove()

    print(data)
