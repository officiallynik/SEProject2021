import sys
sys.path.append("./AnswerSearch")
from flask import Flask, request
from main import getAnswers

app = Flask(__name__)

@app.route('/search')
def search():
    print("[search req]")
    query = request.args.get("query")
    print("query", query)
    json_res = getAnswers(query)
    # print(json_res)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return json_res

# @app.route('/search/summary')
# def search_summary():
#     body = request.form
#     query = body["query"]
#     json_res = getSummarizedAnswer(query)
#     #print(json_res)
#     return json_res

app.debug = False
app.run()
