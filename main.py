import datetime

from selenium import webdriver
import chromedriver_autoinstaller
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError
import time

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{'projectId': 'silversns'})
chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]  #크롬드라이버 버전 확인




def job():
    try:
        driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')
        print('already')
    except:
        chromedriver_autoinstaller.install(True)
        driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')
        print('download')
    # 드라이버 설치과정

    driver.implicitly_wait(10)

    url = "http://rank.ezme.net/nate"

    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    datas = soup.select(
        'body > div.mdl-layout__container > div > main > div > div:nth-child(7) > div:nth-child(15) div span.mdl-chip__text')

    result = []
    for data in datas:
        result.append(data.text)
        print(data.text)

    print(result)
    driver.close()

    db = firestore.client()
    doc_ref = db.collection(u'Hotkey').document(u'hotkey')
    doc_ref.set({
        u'hotkeyword': result,
        u'timestamp': firestore.SERVER_TIMESTAMP
    })

sched = BackgroundScheduler()
sched.start()
sched.add_job(job,'cron',minute='00',second='30',id="test")
while True :
    print("Running process......")
    time.sleep(1)




