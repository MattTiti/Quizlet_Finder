import requests
from bs4 import BeautifulSoup
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        query = request.form["query"]
        google_url = f"https://www.google.com/search?q={query}+site%3Aquizlet.com"
        response = requests.get(google_url)
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("a")
        links = []
        titles = []
        descriptions = []
        # divs = soup.find_all("div")
        # print(divs)
        # for div in divs:
        #     spans = div.find_all("span")
        #     print(spans)
        #     # for span in spans:
        #     #     # Do something with the span element
        #     #     descriptions.append(span.text)
        for result in results:
            if "href" in result.attrs:
                url = result.attrs["href"]
                if url.startswith("/url?q="):
                    url = url[7:]
                    if "quizlet.com" in url:
                        links.append(url)
                        # Extract the title of the Quizlet from the URL
                        title = url.split("/")[-2].replace("-", " ")
                        titles.append(title)
        print(links)
        return render_template("index.html", links=links, titles=titles)
    return render_template("index.html")

if __name__ == "__main__":
    app.run()

