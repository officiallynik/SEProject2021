import sys,os

sys.path.append("./AnswerSearch/QuestionsRetrieval")
#sys.path.append('./AnswerSearch/QuestionsRetrieval')
sys.path.append('./AnswerSearch/AnswersRetrieval')
sys.path.append('./AnswerSearch/Summarizer')
from questionretrieval import retrieve_top_matched_questions
from answersretrieval import retrieve_top_matched_answers
from summarizer import mmr_handler
from html.parser import HTMLParser
import re
import json
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

def search_query(query):
    questions = retrieve_top_matched_questions(query, 5, False)

    sorted_paragraphs=retrieve_top_matched_answers(questions, query)
    final_paragraphs=mmr.rank_mmr(sorted_paragraphs)

    response_paragraphs=[]

    for cnt, para_obj in enumerate(final_paragraphs, 1):
            #print(f"answer no. {cnt}")
            #print("\nanswer:")

            response_paragraphs.append(para_obj["paragraph"].raw_text)
            #print("MMR Score: ",para_obj["mmr_score"])
            #print("--------------------------------------------------------------------------------------------")


    respose={"questions":questions,"answers":response_paragraphs}


    json_res=json.dumps(respose)
    print(json_res)
    return json_res
    




# if __name__=="__main__":
#     get_answer_summary("print in python")
#     while True:
#         inp = input("query > ")
#         if inp == "exit":
#             break
#         inp = inp.split("--")
#         query = inp[0]

#         questions = retrieve_top_matched_questions(query, 5, len(inp)>1)

#         sorted_paragraphs=retrieve_top_matched_answers(questions, query)
#         final_paragraphs=mmr.rank_mmr(sorted_paragraphs)
#         #print(final_paragraphs)
#         print("\n\n")
#         for cnt, para_obj in enumerate(final_paragraphs, 1):
#             #print(f"answer no. {cnt}")
#             #print("\nanswer:")

#             answer_display(para_obj["paragraph"].raw_text)
#             #print("MMR Score: ",para_obj["mmr_score"])
#             print("--------------------------------------------------------------------------------------------")
