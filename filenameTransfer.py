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
prefs = {"download.default_directory": "C:\\Users\\디랩 학생\\Desktop\\crawlingTest"}
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

종목코드들 = []
종목코드별다운로드파일이름 = {}

for n in range(1, 11):
    isKOSPI_KOSDAQ = browser.find_element(By.CSS_SELECTOR,
                                          ".table_list tr:nth-child(" + str(n) + ")>td:nth-child(2)>span>img")
    isKOSPI_KOSDAQ = isKOSPI_KOSDAQ.get_attribute("title")
    if ("유가증권" in isKOSPI_KOSDAQ) or ("코스닥" in isKOSPI_KOSDAQ):
        companyName = browser.find_element(By.CSS_SELECTOR,
                                           ".table_list tr:nth-child(" + str(n) + ")>td:nth-child(2)>span>a")
        companyName.click()
        time.sleep(0.5)
        종목코드 = browser.find_element(By.CSS_SELECTOR, "#pop_body tr:nth-child(4)>td").text
        if not 종목코드 in 종목코드들:
            종목코드들.append(종목코드)
            browser.find_element(By.CSS_SELECTOR, "#ext-gen81").click()
            link = browser.find_element(By.CSS_SELECTOR,
                                        ".table_list tr:nth-child(" + str(n) + ")>td:nth-child(3)>a")  # 보고서 다운로드 링크

            if searchYear in link.text and searchMonth in link.text:
                link.send_keys(Keys.CONTROL + "\n")
                time.sleep(1)

                browser.switch_to.window(browser.window_handles[1])
                browser.find_element(By.XPATH, "//a[@href='#download']").send_keys(Keys.CONTROL + "\n")
                time.sleep(1)

                browser.switch_to.window(browser.window_handles[2])
                downloadFile = browser.find_element(By.CSS_SELECTOR, "table tr:nth-child(2)>td:nth-child(1)").text
                downloadFile = downloadFile.split("(")[1].split(".")[0]
                종목코드별다운로드파일이름[downloadFile] = 종목코드
                browser.find_element(By.CSS_SELECTOR, "table tr:nth-child(2)>td:nth-child(2)>a").send_keys(
                    Keys.CONTROL + "\n")  # 파일 다운로드
                downloadCount += 1
                time.sleep(1)

                browser.close()
                browser.switch_to.window(browser.window_handles[1])
                browser.close()
                browser.switch_to.window(browser.window_handles[0])
                time.sleep(0.5)
        else:
            browser.find_element(By.CSS_SELECTOR, "#ext-gen81").click()

print(종목코드별다운로드파일이름);