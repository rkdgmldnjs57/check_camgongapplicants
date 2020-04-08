import keyboard
import time, os
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import winsound as ws

def beepsound():
    freq = 2000  # range : 37 ~ 32767
    dur = 5000  # ms
    ws.Beep(freq, dur)  # winsound.Beep(frequency, duration)

url = 'http://sjecampus.com/sugang/student/consent_list.php?s_LB_type=H1&LB_area=&LB_school=&LB_subject=%C1%A4%BA%B8%B0%FA%C7%D0&LB_part1=&x=0&y=0&LB_stime=&TT_name='
driver = webdriver.Chrome('./chromedriver')
driver.get(url)
os.makedirs('result', exist_ok=True)
df = pd.DataFrame(columns=['school1', 'applycant1', 'school2', 'applycant2', 'datetime'])
time.sleep(5)
cnt = 0

while (not (keyboard.is_pressed('q'))):
    reviews = driver.find_elements_by_tag_name('tr')
    list = []
    now = datetime.now()
    for review in reviews[9:11]:
        soup = BeautifulSoup(review.get_attribute('innerHTML'), 'html.parser')
        temp = soup.find_all('td')
        for i in temp:
            list.append(i.text)

    df = df.append({
        'school1': list[1],
        'applycant1': list[8],
        'school2': list[10],
        'applycant2': list[17],
        'datetime': str(now)
    }, ignore_index=True)

    if (list[8] != '20' or list[17] != '21'):
        beepsound()

    driver.refresh()

    time.sleep(5)
    cnt += 1

    if cnt % 200 == 0:
        filename = datetime.now().strftime('result/%Y-%m-%d_%H-%M-%S.csv')
        df.to_csv(filename, encoding='utf-8-sig', index=False)

filename = datetime.now().strftime('result/%Y-%m-%d_%H-%M-%S.csv')
df.to_csv(filename, encoding='utf-8-sig', index=False)
driver.stop_client()
driver.close()

print('Done!')
