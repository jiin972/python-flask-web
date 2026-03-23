from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

class WantedScraper:
    #초기 설정(키워드를 받아서 저장)
    def __init__(self, keyword):
        self.keyword = keyword
        self.jobs_db = []
        self.base_url = "https://www.wanted.co.kr"
    #브라우저(헤드레스)띄워서 데이터 가져오기(행동 1)
    #playwirght 실행(with 구문을 사용하면 p.stop()을 자동으로 함)
    def get_page(self):
        with sync_playwright() as p:
            browser = p.firefox.launch(headless = True)
            context = browser.new_context(user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
            page = context.new_page()
            #브라우저 자동화 로직
            page.goto(self.base_url, timeout=60000)
            page.wait_for_load_state("load")
            time.sleep(2)

            if page.query_selector("iframe.ab-in-app-message"):
                page.keyboard.press("Escape")
                time.sleep(2)
            
            page.click("button.searchButton_6a6844fa") # button엘레멘트 중 해당 class 선택, 클릭
            time.sleep(2) #bot감지 우회를 위해, 딜레이추가

            #입력창에 self.keyword 사용
            page.get_by_placeholder("검색어를 입력해 주세요.").fill(self.keyword) #플레이스홀더로 해당 element를 가져
            time.sleep(2)
            page.keyboard.press("Enter") #엔터키 누르고 떼기, down은 떼기는 하지 않음
            time.sleep(2)

            page.click("[data-testid='SearchContentViewMoreButton']") #[]으로 속성 선택,
            time.sleep(2)

            for _ in range(2):
                page.keyboard.press("End")
                time.sleep(0.5)

            #HTML 읽기 및 추출 함수 호출
            content = page.content()
            self.extract_jobs(content)

            browser.close()
        
        return self.jobs_db
    
    def extract_jobs(self, html):
        soup = BeautifulSoup(html, "html.parser")
        jobs = soup.find_all("div", class_="JobCard_container__zQcZs")

        for job in jobs:
            a_tag = job.find("a")
            link = a_tag.get("href") if a_tag else "No link"
            url = self.base_url + link if link.startswith("/") else link

            title_tag = job.find("strong", class_="JobCard_title___kfvj")
            company_tag = job.find("span",class_="CompanyNameWithLocationPeriod_CompanyNameWithLocationPeriod__company__ByVLu wds-nkj4w6")
            career_tag = job.find("span",class_="CompanyNameWithLocationPeriod_CompanyNameWithLocationPeriod__location__4_w0l wds-nkj4w6")
            reward_tag = job.find("span", class_="JobCard_reward__oCSIQ")

            self.jobs_db.append({
                "title" : title_tag.text.strip() if title_tag else "No title",
                "company" : company_tag.text.strip() if company_tag else "No company",
                "career" : career_tag.text.strip() if career_tag else "No career",
                "reward" : reward_tag.text.strip() if reward_tag else "No reward",
                "link" : url
                })