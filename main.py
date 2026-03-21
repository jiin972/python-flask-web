from playwright.sync_api import sync_playwright
import time #코드에 대기시간을 생성하게 해줌(headless모드에서는 필요없을 듯)
from bs4 import BeautifulSoup
import csv
from file import save_to_file

#초기화
p = sync_playwright().start() #playwright 초기화
browser = p.firefox.launch(headless=True) #브라우저 생성 및 초기화
context = browser.new_context(
    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
)
page = context.new_page()


#브라우저 자동화
page.goto("https://www.wanted.co.kr/", timeout=60000)
page.wait_for_load_state("load") #네크워크 요청이 완전히 끝날때 까지 대기
time.sleep(2) #추가 대기(팝업 틀 시간 확)

if page.query_selector("iframe.ab-in-app-message"): #팝업 iframe이 존재하는지 체크
    page.keyboard.press("Escape")
    time.sleep(1)

page.click("button.searchButton_6a6844fa") # button엘레멘트 중 해당 class 선택, 클릭
time.sleep(2) #bot감지 우회를 위해, 딜레이추가

page.get_by_placeholder("검색어를 입력해 주세요.").fill("flutter") #플레이스홀더로 해당 element를 가져
time.sleep(2)

page.keyboard.press("Enter") #엔터키 누르고 떼기, down은 떼기는 하지 않음
time.sleep(2)

page.click("[data-testid='SearchContentViewMoreButton']") #[]으로 속성 선택,
time.sleep(2)

for _ in range(2):
    page.keyboard.press("End")
    time.sleep(0.5)
    
content = page.content() #페이지의 HTML을 읽어옴

browser.close() #브라우저 프로세스 메모리에서 제거
p.stop() #browser.close() 이후에 p.stop()을 해줘야함/ 프로세스정리

#Beautiful soup을 사용해 데이트 스크래이핑
soup = BeautifulSoup(content,"html.parser")
jobs = soup.find_all("div",class_="JobCard_container__zQcZs") #배열을 반환, for문으로 추출

base_url = "https://www.wanted.co.kr"

jobs_db =[] #스크래핑 결과를 담을 빈 리스트

for job in jobs: #job은 soup의 element
    a_tag = job.find("a")
    link = a_tag.get("href") if a_tag else "No link"

    if link and link.startswith("/"): # 링크가 유효하고, 링크가"/"로 시작하면, 
        url = base_url + link
    else:
        url = link or "No URL"

    title_tag = job.find("strong", class_="JobCard_title___kfvj")
    company_tag = job.find("span",class_="CompanyNameWithLocationPeriod_CompanyNameWithLocationPeriod__company__ByVLu wds-nkj4w6")
    career_tag = job.find("span",class_="CompanyNameWithLocationPeriod_CompanyNameWithLocationPeriod__location__4_w0l wds-nkj4w6")
    reward_tag = job.find("span", class_="JobCard_reward__oCSIQ")

#프로그램 crash방지
    title = title_tag.text.strip() if title_tag else "No title"
    company = company_tag.text.strip() if company_tag else "No company"
    career = career_tag.text.strip() if career_tag else "No career"
    reward = reward_tag.text.strip() if reward_tag else "No reward"
    #딕셔너리 생성
    job = {
        "title":title,
        "company":company,
        "career":career,
        "reward":reward,
        "link": url
    }
    jobs_db.append(job) #생성된 딕셔너리를 리스트에 넣음

print(len(jobs_db))
save_to_file("wanted_jobs.csv", jobs_db)
print("csv저장완료")
