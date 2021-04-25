"""

Provides an API for using our PyStackBot Tool

"""

import sys
sys.path.append("./AnswerSearch")
from flask import Flask, request
from main import getAnswers, getSummarizedAnswer
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/search')
def search():
    query=request.args.get('query')
    print(query)
    json_res=getAnswers(query)
    return json_res

@app.route('/search/summary')
def search_summary():
	query=request.args.get('query')
	print(query)
	json_res=getSummarizedAnswer(query)
	return json_res

app.debug = False
app.run()
