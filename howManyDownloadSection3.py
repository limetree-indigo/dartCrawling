from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# 정기 보고서 중에서 사업보고서 다운로드 받고자함
# 유가증권, 코스닥 상장 기업만 다운 받고자 함
# 종목번호 + 연도의 형태로 파일을 다운 받고자함

'''------기본설정----------'''
url = "http://dart.fss.or.kr/"
prefs = {"download.default_directory": "C:\\Users\\UpC\\Desktop\\crawlingTest"}
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

e = browser.find_element(By.ID,  "publicType1")  # 사업보고서 체크박스
browser.execute_script("arguments[0].click();", e)  # 사업보고서 체크박스 체크하기
browser.find_element(By.CSS_SELECTOR, ".btn>.ibtn").click()  # 검색버튼 클릭하기
browser.find_element(By.CSS_SELECTOR, "#maxResultsCb>option:last-child").click()
browser.find_element(By.CSS_SELECTOR, "#searchpng").click()
browser.find_element(By.XPATH, "(//input[@alt='다음'])").click() #page11에서 시작

print(startDate, '~', endDate, ':', '사업보고서(', searchYear, '.', searchMonth, ')', 'page11~15')

종목코드들 = []


for page in range(1, 6):
    print("다운로드 진행상황: ", page+10, '/', 15)
    companies = browser.find_elements(By.CSS_SELECTOR, ".table_list tbody>tr")  # 회사목록

    for n in range(1, len(companies) + 1):
        isKOSPI_KOSDAQ = browser.find_element(By.CSS_SELECTOR, ".table_list tr:nth-child("+str(n)+")>td:nth-child(2)>span>img")
        isKOSPI_KOSDAQ = isKOSPI_KOSDAQ.get_attribute("title")
        if ("유가증권" in isKOSPI_KOSDAQ) or ("코스닥" in isKOSPI_KOSDAQ):
            companyName = browser.find_element(By.CSS_SELECTOR, ".table_list tr:nth-child("+str(n)+")>td:nth-child(2)>span>a")
            companyName.click()
            time.sleep(0.5)
            종목코드 = browser.find_element(By.CSS_SELECTOR, "#pop_body tr:nth-child(4)>td").text
            if not 종목코드 in 종목코드들:
                종목코드들.append(종목코드)
                browser.find_element(By.CSS_SELECTOR, "#ext-gen81").click()

            else:
                browser.find_element(By.CSS_SELECTOR, "#ext-gen81").click()

    if page<5:
        browser.find_element(By.XPATH, "(//input[@type='button'])["+str(page)+"]").click()
    browser.implicitly_wait(3)

time.sleep(0.5)
browser.close()
print('다운로드 파일 개수:', len(종목코드들), '건')