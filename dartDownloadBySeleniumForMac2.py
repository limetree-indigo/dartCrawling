from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time


'''------기본설정----------'''
url = "http://dart.fss.or.kr/"
prefs = {"download.default_directory": "C:\\Users\\UpC\\Desktop\\crawlingTest"}
chromeOptions = Options()
chromeOptions.add_experimental_option("prefs", prefs)
chromeDriver = "C:/Users/UpC/Desktop/webcrawling/python-crawling/chromedriver.exe"
serv = Service(chromeDriver)
browser = webdriver.Chrome(service=serv, options=chromeOptions)
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

pages = browser.find_elements(By.XPATH, "//input[@type='button']") # 검색 페이지 수

totalPageNumber = browser.find_element(By.CSS_SELECTOR, ".page_info").text.split(']')
totalPageNumber = totalPageNumber[0].split('/')
totalPageNumber = int(totalPageNumber[1])

print(startDate, '~', endDate, ':', '감사보고서(', searchYear, '.', searchMonth, ')')

for page in range(1, totalPageNumber+1):
    print("다운로드 진행상황: ", page, '/', totalPageNumber)
    companies = browser.find_elements(By.CSS_SELECTOR, ".table_list tbody>tr")  # 회사목록
    for num in range(1, len(companies)+1):
        companyName = browser.find_element(By.CSS_SELECTOR, ".table_list tr:nth-child("+str(num)+")>td:nth-child(2)>span>a")     # 회사명
        link = browser.find_element(By.CSS_SELECTOR, ".table_list tr:nth-child("+str(num)+")>td:nth-child(3)>a") # 보고서 다운로드 링크

        if searchYear in link.text and searchMonth in link.text:
            link.send_keys(Keys.CONTROL + "\n")
            time.sleep(1)

            browser.switch_to.window(browser.window_handles[1])
            browser.find_element(By.XPATH, "//a[@href='#download']").send_keys(Keys.CONTROL + "\n")
            time.sleep(1)
            browser.switch_to.window(browser.window_handles[2])
            browser.find_element(By.CSS_SELECTOR, "table tr:nth-child(2)>td:nth-child(2)>a").send_keys(Keys.CONTROL + "\n") # 파일 다운로드
            downloadCount += 1
            time.sleep(1)
            browser.close()
            browser.switch_to.window(browser.window_handles[1])
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
            time.sleep(0.5)

    # 페이지 이동
    if (page % 10) and (page != totalPageNumber):
        browser.find_element(By.XPATH, "(//input[@type='button'])["+str(page%10)+"]").click()
    if (not (page % 10)) and (page != totalPageNumber):
        browser.find_element(By.XPATH, "(//input[@alt='다음'])").click()

print("다운로드링크 수 : ", downloadCount)




