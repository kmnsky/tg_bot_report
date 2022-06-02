# data analysis and wrangling
import pandas as pd
import numpy as np
import re
from datetime import datetime
import pickle
import time
import random
from config import username, password

# Web
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Writing multiple dataframes to worksheets using Pandas and XlsxWriter
import xlsxwriter
import os
import pathlib
from pathlib import Path

def rounder(t):
    """Rounding time to the hour"""
    if t.minute >= 30:
        return t.replace(second=0, microsecond=0, minute=0, hour=t.hour+1).strftime('%H_%M')
    else:
        return t.replace(second=0, microsecond=0, minute=0).strftime('%H_%M')

now = datetime.now()

path_fb = Path(pathlib.Path.cwd(), "Статистика команды.xlsx")
path_fb_report = Path(pathlib.Path.cwd(), f"Fbtool_{rounder(now)}.xlsx")
path_driver = Path(pathlib.Path.cwd(), 'chromedriver')

def delete_files(file_name):
    """Delete files from a directory"""
    path = os.path.join(os.path.abspath(os.path.dirname(file_name)), file_name)
    os.remove(path)


def upload_file_fbtool():
    """Loading statistics file from Fbtool"""
    # options
    options = webdriver.ChromeOptions()
    # user-agent
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36")
    # disable webdriver mode
    options.add_argument("--disable-blink-features=AutomationControlled")
    # # headless mode
    options.add_argument("--headless")
    driver = webdriver.Chrome(path_driver, options=options)

    print('Going to the Fbtool')
    driver.get('https://fbtool.pro/login')
    time.sleep(random.randrange(3, 6))
    # username_input = driver.find_element_by_name('username')
    # username_input.clear()
    # username_input.send_keys(username)
    # time.sleep(20)

    # password_input = driver.find_element_by_name('password')
    # password_input.clear()
    # password_input.send_keys(password)
    # password_input.send_keys(Keys.ENTER)
    # time.sleep(8)

    # # # cookies
    # pickle.dump(driver.get_cookies(), open("fbtool_cookies", "wb"))

    for cookie in pickle.load(open("fbtool_cookies", "rb")):
        driver.add_cookie(cookie)

    time.sleep(random.randrange(3, 6))
    driver.refresh()
    time.sleep(random.randrange(3, 7))

    print('Open statistics')
    driver.get('https://fbtool.pro/team/statistics?dates=&status=&currency=&adaccount_status=&ad_account_id=all&id=all')
    time.sleep(random.randrange(9, 13))

    try:
        select_adset = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/form/div/select')
        select_adset.click()
    except Exception as ex:
        print(ex)

    time.sleep(random.randrange(2, 4))

    try:
        adset = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/form/div/select/option[2]')
        adset.click()
    except Exception as ex:
        print(ex)

    time.sleep(random.randrange(3, 5))
    print('Download file')
    download_file = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div[2]/div[1]/div[4]/div/div/div/div[1]/button[2]')
    download_file.click()
    time.sleep(random.randrange(3, 8))

    driver.close()
    driver.quit()

def fbtool_report():
    xls = pd.ExcelFile(path_fb)
    fb = pd.read_excel(xls, 'Sheet1', header=1)
    fb.dropna(axis='columns',how='all', inplace=True)

    fb = fb.assign(CPI =  fb.Расход/fb.Установки)
    # Replace Inf
    fb.replace([np.inf, -np.inf, np.nan], 0, inplace=True)
    # Two decimal places
    fb = fb.round(decimals=2)

    # Adset split
    fb_adset = fb['Адсет'].str.split('_', expand=True)[[4,5,17]]
    fb_adset[17] = fb_adset[17].str.split('ии - ', expand=True)[1].str.split(' ', expand=True)[0]

    # Renaming columns
    fb_adset = fb_adset.rename(columns=
                           {4: 'soc',
                            5: 'bm',
                            17: 'Дневной_бюджет'
                           })

    fb = pd.concat([fb, fb_adset],axis=1)


    fb_slit = fb['Кабинет'].str.split(':', expand=True)

    fb_slit[0] = fb_slit[0].str.split(')', expand=True)[1].str.split('Л', expand=True)[0]

    fb_slit_1 = fb_slit[2].copy()
    fb_slit_1 = fb_slit_1.str.split(' ', expand=True)[1].str.split('/', expand=True)

    # Renaming columns
    fb_slit_1 = fb_slit_1.rename(columns=
                           {0: 'Билинг_Отлито',
                            1: 'Билинг_Тотал',
                           })

    fb_slit.drop([1, 3], axis=1, inplace=True)

    fb_slit['Бин'] = fb['Кабинет'].str.split('*', expand=True)[1].str.split('О', expand=True)[0].copy()

    fb_slit_final = pd.concat([fb_slit, fb_slit_1],axis=1)

    fb_slit_final.drop(2, axis=1, inplace=True)

    # Renaming columns
    fb_slit_final = fb_slit_final.rename(columns=
                           {0: 'Статус_Кабинет',
                            3: 'Бин',
                           })

    fb_slit_final = fb_slit_final[['Статус_Кабинет', 'Билинг_Отлито', 'Билинг_Тотал', 'Бин',]]

    fb_slit_final['Билинг_Отлито'].replace(['VISA', 'Mastercard'], 0, inplace=True)
    fb_slit_final['Билинг_Тотал'].replace(np.nan, 0, inplace=True)

    fb_slit_final['Билинг_Отлито'].replace(np.nan, 0, inplace=True)

    fb_slit_final['Билинг_Отлито'] = fb_slit_final['Билинг_Отлито'].astype(int)
    fb_slit_final['Билинг_Тотал'] = fb_slit_final['Билинг_Тотал'].astype(int)

    fb = pd.concat([fb, fb_slit_final],axis=1)

    # Renaming columns
    fb = fb.rename(columns=
                           {'Клики по ссылке': 'Клики',
                           })

    fb = fb.sort_values(['Статус_Кабинет', 'Расход'], ascending=[False, False])

    fb['Статус_Кабинет'].replace('АктивенБиллинг', 'Активен', inplace=True)
    fb['Статус_Кабинет'].replace('DISABLEDADS_INTEGRITY_POLICYБиллинг', 'DISABLEDADS_INTEGRITY_POLICY', inplace=True)

    ## File save

    print('File save')
    now = datetime.now()

    writer = pd.ExcelWriter(f"Fbtool_{rounder(now)}.xlsx", engine='xlsxwriter')

    # Write each dataframe to a different worksheet.
    fb.to_excel(writer, sheet_name='Sheet1', index=False)

    # # Get the xlsxwriter workbook and worksheet objects.
    workbook  = writer.book
    worksheet_Pivot = writer.sheets['Sheet1']

    # Number Format Categorie
    currency_format = workbook.add_format({'num_format':
                                           '_-* # ##0_-;-* # ##0_-;_-* "-"??_-;_-@_-'})
    center = workbook.add_format({'align': 'center'})

    # # # Set the column width and format.
    worksheet_Pivot.set_column('M:M', 18, center)
    worksheet_Pivot.set_column('N:N', 27)
    worksheet_Pivot.set_column('K:L', 18)
    worksheet_Pivot.set_column('O:P', 18)
    worksheet_Pivot.set_column('Q:Q', 12, center)

    writer.save()

def upload_file_keitaro():
    """Loading statistics file from Fbtool"""
    # options
    options = webdriver.ChromeOptions()
    # user-agent
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36")
    # disable webdriver mode
    options.add_argument("--disable-blink-features=AutomationControlled")
    # # headless mode
    options.add_argument("--headless")

    driver = webdriver.Chrome(path_driver, options=options)
    driver.get('https://tds4.pleione.co/admin/?#!/campaigns/')
    time.sleep(random.randrange(3, 5))

    username_input = driver.find_element_by_name('login')
    username_input.clear()
    username_input.send_keys(username)

    time.sleep(3)

    password_input = driver.find_element_by_name('password')
    password_input.clear()
    password_input.send_keys(password)
    password_input.send_keys(Keys.ENTER)
    time.sleep(3)

    print('Open statistics')
    driver.get("https://tds4.pleione.co/admin/?#!/reports/favourite/55/?s=~(grouping~(~'day~'campaign~'sub_id_3)~metrics~(~'clicks~'campaign_unique_clicks~'conversions~'sales)~limit~null~range~(interval~'today~timezone~'Europe*2fMoscow)~filters~(~(disabled~false~name~'campaign_group_id~operator~'IN_LIST~expression~(~10)~!!hashKey~'object*3a1143))~resized_columns~(sub_id_2~147~sub_id_3~832))")
    time.sleep(random.randrange(9, 13))

    print('File export')
    try:
        select_export = driver.find_element_by_xpath('/html/body/layout/div/snap-content/div/div[2]/div/div/app-report/grid-footer-navi/div/div[2]/div/grid-export/div/button')
        select_export.click()
    except Exception as ex:
        print(ex)

    try:
        select_csv = driver.find_element_by_xpath('/html/body/layout/div/snap-content/div/div[2]/div/div/app-report/grid-footer-navi/div/div[2]/div/grid-export/div/ui/li[1]/a')
        select_csv.click()
    except Exception as ex:
        print(ex)

    time.sleep(random.randrange(3, 6))

    driver.close()
    driver.quit()

if __name__ == '__main__':
    upload_file_fbtool()
    fbtool_report()
    upload_file_keitaro()
