import sys
sys.path.append('./AnswerSearch/PreProcessor')
from elasticsearch import Elasticsearch
from paragraph import Paragraph
from preprocessor import PreprocessPostContent
from html.parser import HTMLParser
import nltk
import re
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        print(data)

parserHTML = MyHTMLParser()

def get_answers_list(qid):
    # Query Passed by user
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    doc = {
        "query": {
            "bool": {
                "should": [
                    {"match": {"parent_id": qid}}
                ]
            }
        }
    }
    returned_answers = es.search(
        index="answerbot_answers", body=doc)
    relevant_answers = []
    for res in returned_answers['hits']['hits']:
        relevant_answers.append(res['_source'])

    return relevant_answers

def process_answers(answer_list):
    preprocessor = PreprocessPostContent()
    paragraph_obj_list = []
    for answer in answer_list:
        paragraph_list = preprocessor.getParagraphs(answer['body'])
        for pos, para in enumerate(paragraph_list, 1):
            paragraph_obj_list.append(
                Paragraph(para, preprocessor.get_single_para_word_list(para), vote_score=int(answer['score']), position=pos))

    return paragraph_obj_list

def sort_paragraphs(paragraph_obj_list, query):
    # calculate score and sort
    preprocessor = PreprocessPostContent()
    preprocessed_query = preprocessor.get_single_para_word_list(query)
    query_tokens = nltk.word_tokenize(preprocessed_query)
    relevance_list = []
    entropy_list = []
    vote_score_list = []
    for para_obj in paragraph_obj_list:
        para_obj.cal_relevance(query_tokens)
        para_obj.cal_entropy()
        para_obj.cal_semantic_pattern()
        para_obj.cal_format_pattern()
        relevance_list.append(para_obj.relevance_score)
        entropy_list.append(para_obj.infor_entropy)
        vote_score_list.append(para_obj.vote_score)

    for para_obj in paragraph_obj_list:
        para_obj.normalized(min(relevance_list), max(relevance_list), min(entropy_list), max(entropy_list),
                            min(vote_score_list), max(vote_score_list))
        para_obj.cal_overall_score()

    paragraph_obj_list.sort(reverse=True)

    return paragraph_obj_list

def answer_display(answer_raw):
    processed_answer = re.sub(r"<.*?>", "", answer_raw)
    processed_answer = re.sub(r"</.*?>", "", processed_answer)
    parserHTML.feed(processed_answer)

def retrieve_top_matched_answers(questions, query):
    answer_list_list = []
    for question in questions:
        answer_list_list.append(get_answers_list(question['question']['id']))
    #print(answer_list_list)
    answer_obj_list = []
    for answer_list in answer_list_list:
        answer_obj_list.extend(process_answers(answer_list))

    answer_obj_list_sorted = sort_paragraphs(answer_obj_list, query)
    answer_obj_list_sorted = answer_obj_list_sorted[:10]

    # for cnt, para_obj in enumerate(answer_obj_list_sorted, 1):
    #     print(f"answer no. {cnt}")
    #     print("\nanswer:")
    #     answer_display(para_obj.raw_text)
    #     print("Score: ",para_obj.overall_score)
    #     print("--------------------------------------------------------------------------------------------\n\n")
    
    return answer_obj_list_sorted

if __name__ == '__main__':
    pass
    # testing
    # print(get_answers_list('43432675'))
    # query = "sort array in reverse"

    # answer_list_list = []
    # answer_list_list.append(get_answers_list('43432675'))

    # paragraph_obj_list = []
    # for answer_list in answer_list_list:
    #     paragraph_obj_list.extend(process_answers(answer_list))

    # paragraph_obj_list_sorted = sort_paragraphs(paragraph_obj_list, query)
    # for cnt, para_obj in enumerate(paragraph_obj_list_sorted, 1):
    #     print("answer no.", cnt)
    #     print("overall score:", para_obj.overall_score)
    #     print("body:")
    #     answer_display(para_obj.raw_text)
    #     print("---------------------------\n\n")