import sys
sys.path.append("./AnswerSearch")
from flask import Flask,request
from main import getAnswers,getSummarizedAnswer

app=Flask(__name__)

@app.route('/search')
def search():
    body=request.form
    query=body["query"]
    json_res=getAnswers(query)
    #print(json_res)
    return json_res

@app.route('/search/summary')
def search_summary():
    body=request.form
    query=body["query"]
    json_res=getSummarizedAnswer(query)
    #print(json_res)
    return json_res

app.debug = True
app.run()
app.run(debug = True)
