import sys,os
sys.path.append("./AnswerSearch/QuestionsRetrieval")
sys.path.append('./AnswerSearch/AnswersRetrieval')
sys.path.append('./AnswerSearch/Summarizer')
from questionretrieval import retrieve_top_matched_questions
from answersretrieval import retrieve_top_matched_answers,retrieve_top_matched_answer_paragraphs
from summarizer import mmr_handler
import re
import json
from html.parser import HTMLParser
mmr=mmr_handler()

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        print(data)


parserHTML = MyHTMLParser()

def answer_display(answer_raw):
    processed_answer = re.sub(r"<.*?>", "", answer_raw)
    processed_answer = re.sub(r"</.*?>", "", processed_answer)
    parserHTML.feed(processed_answer)


def getAnswers(query):
    """
    Returns Relevant Answers to the user query

    Parameters:
    query (string): User query

    Returns:
    json: 
        questions: Top matched questions
        answers:  Top matched answers

   """
    questions = retrieve_top_matched_questions(query, 5, False)
    answers_list=retrieve_top_matched_answers(questions,query)
    final_answers_list=[]
    for answer in answers_list:
        final_answers_list.append(answer['answer'])
    respose={"questions":questions,"answers":final_answers_list}
    json_res=json.dumps(respose)
    return json_res

def getSummarizedAnswer(query):
    """
    Generated a summarized answer for the passed User Query.

    Parameters:
    query (string): User Query

    Returns:
    json: 
        questions: Top matched questions
        answers:  paragraphs of summarized answer

   """
    questions = retrieve_top_matched_questions(query, 5, False)

    sorted_paragraphs=retrieve_top_matched_answer_paragraphs(questions, query)
    final_paragraphs=mmr.rank_mmr(sorted_paragraphs)

    response_paragraphs=[]

    for cnt, para_obj in enumerate(final_paragraphs, 1):
            response_paragraphs.append(para_obj["paragraph"].raw_text)


    respose={"questions":questions,"answers":response_paragraphs}


    json_res=json.dumps(respose)
    return json_res


if __name__=="__main__":
    """

    Using PyStackBot from CLI

    """
    while True:
        inp = input("query > ")
        if inp == "exit":
            break
        inp = inp.split("--")
        query = inp[0]
        
        questions = retrieve_top_matched_questions(query, 5, len(inp)>1)
        
        sorted_paragraphs=retrieve_top_matched_answer_paragraphs(questions, query)
        final_paragraphs=mmr.rank_mmr(sorted_paragraphs)
        for cnt, para_obj in enumerate(final_paragraphs, 1):
            answer_display(para_obj["paragraph"].raw_text)
            print("--------------------------------------------------------------------------------------------")
