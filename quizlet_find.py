import os
from googleapiclient.discovery import build
from flask import Flask, request, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = "secretkey123"


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        query = request.form["query"]
        service = build("customsearch", "v1", developerKey='AIzaSyB0Y2mhvYWOmFCFj35rA_8FJKGYEGonkQ0')
        result = service.cse().list(q=query, cx='756fae1a68b4e48dd').execute()
        
        links = []
        titles = []
        descriptions = []
        for item in result['items']:
            link = item['link']
            snip = item['snippet']
            descriptions.append(snip)
            if link.startswith("https://quizlet.com/"):
                links.append(link)
                titles.append(item['title'])
                descriptions.append(item['snippet'])
        return render_template("index.html", links=links, titles=titles, descriptions=descriptions)
    return render_template("index.html")

if __name__ == "__main__":
    app.run()

