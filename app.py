from flask import Flask, render_template, request, redirect,send_file
from scraper import WantedScraper
from file import save_to_file


app = Flask("JobScraper")


db = {} #가짜 데이터베이스 생성(캐시역할, 딕셔너리)

@app.route("/")
def home():
    return render_template("home.html", name = "jin")

@app.route("/search")
def search():
    keyword = request.args.get("keyword") #request.args의 data에서 필요한 부분은 .get()함수로 추출
    #키워드 없을 때, 방어코드 작성
    if keyword == None:
        return redirect("/")

    if keyword in db:
        jobs=db[keyword]
    else:
        #인스턴스 생성
        scraper = WantedScraper(keyword)
        #결과 리스트 받기
        jobs = scraper.get_page()
        db[keyword] = jobs
    return render_template("search.html", name="jin" , keyword=keyword, jobs = jobs)
        

@app.route("/export")
def export():
    keyword = request.args.get("keyword") #request.args의 data에서 필요한 부분은 .get()함수로 추출
    #키워드 없이 url접근  방어코드 
    if keyword == None:
        return redirect("/")
    #db에 없는 키워드 접근 시 방어코드
    if keyword not in db:
        return redirect(f"/search?keyword={keyword}") #키워드가 없을 경우, 검색페이지 강제 이동
    #파일저장로직
    save_to_file(keyword,db[keyword])
    return send_file(f"{keyword}.csv", as_attachment=True)



#서버작동, 맨 마지막에 실행
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4549, debug=True)