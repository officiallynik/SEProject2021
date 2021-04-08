import sys
sys.path.append("./AnswerSearch")
from flask import Flask,request
from main import search_query

app=Flask(__name__)

@app.route('/search')
def hello_world():
    body=request.form
    query=body["query"]
    json_res=search_query(query)
    print(json_res)
    return json_res

app.debug = True
app.run()
app.run(debug = True)

