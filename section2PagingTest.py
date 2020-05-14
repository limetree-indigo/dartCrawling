from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os

# 정기 보고서 중에서 사업보고서 다운로드 받고자함
# 유가증권, 코스닥 상장 기업만 다운 받고자 함
# 종목번호 + 연도의 형태로 파일을 다운 받고자함

'''------기본설정----------'''
url = "http://dart.fss.or.kr/dsab002/main.do"
downloadFolder = "C:\\Users\\UpC\\Desktop\\crawlingTest\\"
prefs = {"download.default_directory": downloadFolder}
chromeOptions = Options()
chromeOptions.add_experimental_option("prefs", prefs)
chromeDriver = "C:/Users/디랩 학생/Desktop/dartCrawling/chromedriver.exe"

browser = webdriver.Chrome(chromeDriver, options=chromeOptions)
browser.implicitly_wait(5)
browser.get(url)

now = time.localtime()
nowYear = str(now.tm_year)
nowMonth = str(now.tm_mon)
nowDay = str(now.tm_mday)
if now.tm_mon < 10:
    nowMonth = "0"+nowMonth
if now.tm_mday < 10:
    nowDay = "0"+nowDay

startDate = "20200102"
endDate = nowYear + nowMonth + nowDay

searchYear = "2019"


# 사업보고서 다운로드 시작
e = browser.find_element(By.ID, "startDate")
e.clear() # 시작 일자 입력
browser.find_element(By.ID, "ext-gen116").click()
e.send_keys(startDate)

e = browser.find_element(By.ID, "endDate") # 마지막 일자 입력
e.clear()
e.send_keys(endDate)

browser.find_element(By.CSS_SELECTOR, "#corporationType option:nth-child(2)").click()

browser.find_element(By.CSS_SELECTOR, "#closingAccountsMonth option:nth-child(2)").click()

e = browser.find_element(By.ID,  "publicType1")  # 사업보고서 체크박스
browser.execute_script("arguments[0].click();", e)

browser.find_element(By.CSS_SELECTOR, "#maxResultsCb option:last-child").click()

browser.find_element(By.ID, "searchpng").click()

browser.find_element(By.XPATH, "(//input[@type='button'])[5]").click()

종목번호들 = []


for page in range(6, 9):
    print("다운로드 진행상황: ", page, '/', 8)

    if page<8:
        browser.find_element(By.XPATH, "(//input[@type='button'])["+str(page)+"]").click()
    browser.implicitly_wait(3)
    time.sleep(2)