from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

'''------기본설정----------'''
url = "http://dart.fss.or.kr/"
chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory":"/Users/jhyoun/Desktop/downTest1"}
chromeOptions.add_experimental_option("prefs", prefs)
chromeDriver = "/Users/jhyoun/Desktop/python-crawling/chromedriver"
browser = webdriver.Chrome(executable_path=chromeDriver, options=chromeOptions)
browser.implicitly_wait(3)
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
e = browser.find_element_by_id("startDate") # 시작 일자 입력
e.clear()
e.send_keys(startDate)
e = browser.find_element_by_id("endDate") # 마지막 일자 입력
e.clear()
e.send_keys(endDate)

e = browser.find_element_by_id("publicType33")  # 감사보고서 체크박스
browser.execute_script("arguments[0].click();", e)  # 감사보고서 체크박스 체크하기
browser.find_element_by_css_selector(".btn>.ibtn").click()  # 검색버튼 클릭하기
browser.find_element_by_css_selector("#maxResultsCb>option:last-child").click()
browser.find_element_by_css_selector("#searchpng").click()

pages = browser.find_elements_by_xpath("//input[@type='button']") # 검색 페이지 수

for page in range(0, len(pages)+1):
    companies = browser.find_elements_by_css_selector(".table_list tbody>tr")  # 회사목록
    for num in range(1, len(companies)+1):
        companyName = browser.find_element_by_css_selector(".table_list tr:nth-child("+str(num)+")>td:nth-child(2)>span>a")     # 회사명
        link = browser.find_element_by_css_selector(".table_list tr:nth-child("+str(num)+")>td:nth-child(3)>a") # 보고서 다운로드 링크

        if searchYear in link.text and searchMonth in link.text:
            link.send_keys(Keys.COMMAND + "\n") # 맥
            # link = browser.find_element_by_css_selector(".table_list tr:nth-child(1)>td:nth-child(3)>a").send_keys(Keys.CONTROL + "\n") # 윈도우용

            time.sleep(1)
            browser.switch_to.window(browser.window_handles[1])
            browser.find_element_by_xpath("//a[@href='#download']").send_keys(Keys.COMMAND + "\n")
            time.sleep(1)
            browser.switch_to.window(browser.window_handles[2])
            browser.find_element_by_css_selector("table tr:nth-child(2)>td:nth-child(2)>a").send_keys(Keys.COMMAND + "\n") # 파일 다운로드
            downloadCount += 1
            time.sleep(1)
            browser.close()
            browser.switch_to.window(browser.window_handles[1])
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
            time.sleep(0.5)
    if page<(len(pages)):
        browser.find_element_by_xpath("(//input[@type='button'])["+str(page+1)+"]").click()

print("다운로드링크 수 : ", downloadCount)




