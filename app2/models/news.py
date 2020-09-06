from flask import Flask, jsonify
from flask_cors import CORS
from newsapi import NewsApiClient


app = Flask(__name__)
CORS(app)

 
@app.route('/news')
def search_news():
    newsapi = NewsApiClient(api_key="ec8c9d047f474773ba7a8157570e4830")
    # define query -> q

    topheadlines = newsapi.get_everything(q="finance", sources="bbc-news,bloomberg,business-insider,fortune,the-verge", sort_by='relevancy')
    #dump(topheadlines)
    return jsonify(topheadlines)
 
 
if __name__ == "__main__":
    app.run(port = 5200, debug=True)