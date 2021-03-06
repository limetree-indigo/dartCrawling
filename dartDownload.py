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




종목번호들 = []


for page in range(1, 5):
    print("다운로드 진행상황: ", page, '/', 5)
    회사들 = browser.find_elements(By.CSS_SELECTOR, "#listContents>div>table>tbody>tr")

    for i in range(1, len(회사들)+1):
        selectedElement = "#listContents>div>table>tbody>tr:nth-child("+ str(i) +")>td:nth-child(2) a"
        browser.find_element(By.CSS_SELECTOR, selectedElement).click()
        time.sleep(0.5)
        종목번호 = browser.find_element(By.CSS_SELECTOR, "#pop_body>div>table>tbody>tr:nth-child(4)>td").text
        종목번호들.append(종목번호)
        browser.find_element(By.ID, "ext-gen151").click()

        selectedElement = "#listContents>div>table>tbody>tr:nth-child(" + str(i) + ")>td:nth-child(3) a"
        downloadLink = browser.find_element(By.CSS_SELECTOR, selectedElement)

        if searchYear in downloadLink.text:
            downloadLink.send_keys(Keys.CONTROL+"\n")
            time.sleep(1)

            browser.switch_to.window(browser.window_handles[1])
            browser.find_element(By.CSS_SELECTOR, "#north>div.view_search>ul>li:nth-child(1)>a").send_keys(Keys.CONTROL + "\n")
            time.sleep(1)

            browser.switch_to.window(browser.window_handles[2])
            downloadfile = browser.find_element(By.CSS_SELECTOR, "body>div>div>table>tbody>tr:nth-child(2)>td:nth-child(1)").text
            downloadfile = downloadfile.split('(')[1].split('.')[0]
            browser.find_element(By.CSS_SELECTOR, "body>div>div>table>tbody>tr:nth-child(2)>td:nth-child(2)>a").send_keys(Keys.CONTROL+"\n")
            time.sleep(1)

            browser.close()
            browser.switch_to.window(browser.window_handles[1])
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
            time.sleep(0.5)

            time.sleep(1)
            os.rename(downloadFolder+downloadfile+".pdf", downloadFolder+종목번호+".pdf")
    if page<4:
        browser.find_element(By.XPATH, "(//input[@type='button'])["+str(page)+"]").click()






# print(종목번호들)
# print(len(종목번호들))
