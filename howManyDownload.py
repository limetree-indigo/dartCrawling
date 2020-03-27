from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time


'''------기본설정----------'''
url = "http://dart.fss.or.kr/"
chromeDriver = "C:/Users/UpC/Desktop/webcrawling/python-crawling/chromedriver.exe"
serv = Service(chromeDriver)
browser = webdriver.Chrome(service=serv)
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

startDate = "20200115"
endDate = nowYear + nowMonth + nowDay

searchYear = "2019"
searchMonth = "12"
downloadCount = 0

'''------감사보고서 검색시작----------'''
e = browser.find_element(By.ID, "startDate") # 시작 일자 입력
e.clear()
e.send_keys(startDate)
e = browser.find_element(By.ID, "endDate") # 마지막 일자 입력
e.clear()
e.send_keys(endDate)

e = browser.find_element(By.ID,  "publicType33")  # 감사보고서 체크박스
browser.execute_script("arguments[0].click();", e)  # 감사보고서 체크박스 체크하기
browser.find_element(By.CSS_SELECTOR, ".btn>.ibtn").click()  # 검색버튼 클릭하기
browser.find_element(By.CSS_SELECTOR, "#maxResultsCb>option:last-child").click()
browser.find_element(By.CSS_SELECTOR, "#searchpng").click()

browser.implicitly_wait(3)
totalPageNumber = browser.find_element(By.CSS_SELECTOR, ".page_info").text.split(']')
totalPageNumber = totalPageNumber[0].split('/')
totalPageNumber = int(totalPageNumber[1])

for page in range(1, totalPageNumber + 1):
    downloadCompanies = browser.find_elements(By.CSS_SELECTOR, ".table_list tbody>tr")  # 회사목록
    for num in range(1, len(downloadCompanies)+1):
        link = browser.find_element(By.CSS_SELECTOR, ".table_list tr:nth-child("+str(num)+")>td:nth-child(3)>a") # 보고서 다운로드 링크

        if (searchYear in link.text) and (searchMonth in link.text):
            downloadCount += 1

    if (page % 10) and (page != totalPageNumber):
        browser.find_element(By.XPATH, "(//input[@type='button'])[" + str(page % 10) + "]").click()
    if (not (page % 10)) and (page != totalPageNumber):
        browser.find_element(By.XPATH, "(//input[@alt='다음'])").click()
    browser.implicitly_wait(3)

time.sleep(0.5)
browser.close()
print(startDate, '~', endDate, ':', '감사보고서(', searchYear, '.', searchMonth, ')')
print(downloadCount, '건')





