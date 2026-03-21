from flask import Flask, render_template, request

app = Flask("JobScraper")

@app.route("/")
def home():
    return render_template("home.html", name = "jin")

@app.route("/search")
def hello():
    keyword = request.args.get("keyword")
    return render_template("search.html", name="jin" , keyword=keyword)
    


#서버작동, 맨 마지막에 실행
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4549, debug=True)