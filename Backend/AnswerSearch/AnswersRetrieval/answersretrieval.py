import sys
sys.path.append('./AnswerSearch/PreProcessor')
from elasticsearch import Elasticsearch
from paragraph import Paragraph
from preprocessor import PreprocessPostContent
import nltk
import re

def get_answers_list(qid):

    """
    Extracts the StackOverFlow Answers from ElasticSearch Server

    Parameters:
    qid (string): ID of the StackOverFlow question whose answers are to be extracted

    Returns:
    list: Extracted Answers

   """
    
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
    """
    Converts the whole answer into a paragraph object

    Parameters:
    answer_list (list): All Relevant Answers extracted from ElasticSearch Server

    Returns:
    list: 
        Type: Dictionary
        Keys:
            'answer': Contains the original Answer Object from StackOverFlow Server
            'para_object': Contains the paragraph object created from body of the original answer

   """
    
    preprocessor = PreprocessPostContent()
    paragraph_obj_list = []
    for answer in answer_list:
        paragraph_obj_list.append({'answer':answer,
        'para_object':(Paragraph(answer['body'], preprocessor.get_single_para_word_list(answer['body']), vote_score=int(answer['score']), position=1))})

    return paragraph_obj_list

def process_answers_into_paragraphs(answer_list):
    """
    Splits the answers into paragraphs and then convert them into paragraph objects

    Parameters:
    answer_list (list): All Relevant Answers extracted from ElasticSearch Server

    Returns:
    list: 
        Type: Paragraph Object
        Description: Paragraph Objects created from paragraphs of the answers passed

   """
    preprocessor = PreprocessPostContent()
    paragraph_obj_list = []
    for answer in answer_list:
        paragraph_list = preprocessor.getParagraphs(answer['body'])
        for pos, para in enumerate(paragraph_list, 1):
            paragraph_obj_list.append(
                Paragraph(para, preprocessor.get_single_para_word_list(para), vote_score=int(answer['score']), position=pos))

    return paragraph_obj_list

def sort_answers(paragraph_obj_list, query):
    """
    Calculates the score of whole answer and sorts them

    Parameters:
    paragraph_obj_list (list): All Relevant Answers converted into Paragraph Objects
    query (string) : Text Query whose answers are to be found

    Returns:
    list: 
        Type: Paragraph Object
        Description: Sorted Paragraph Object List

   """
    preprocessor = PreprocessPostContent()
    preprocessed_query = preprocessor.get_single_para_word_list(query)
    query_tokens = nltk.word_tokenize(preprocessed_query)
    relevance_list = []
    entropy_list = []
    vote_score_list = []
    for answer in paragraph_obj_list:
        para_obj=answer['para_object']
        para_obj.cal_relevance(query_tokens)
        para_obj.cal_entropy()
        para_obj.cal_semantic_pattern()
        para_obj.cal_format_pattern()
        relevance_list.append(para_obj.relevance_score)
        entropy_list.append(para_obj.infor_entropy)
        vote_score_list.append(para_obj.vote_score)

    for answer in paragraph_obj_list:
        para_obj=answer['para_object']
        para_obj.normalized(min(relevance_list), max(relevance_list), min(entropy_list), max(entropy_list),
                            min(vote_score_list), max(vote_score_list))
        para_obj.cal_overall_score()

    paragraph_obj_list.sort(key=lambda x: x['para_object'],reverse=True)

    return paragraph_obj_list

def sort_paragraphs(paragraph_obj_list, query):
    """
    Calculates the score of paragraphs and sort them

    Parameters:
    paragraph_obj_list (list): All Relevant Answer Paragraphs converted into Paragraph Objects
    query (string) : Text Query whose answer summary is to be created

    Returns:
    list: 
        Type: Paragraph Object
        Description: Sorted Paragraph Object List

   """
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

def retrieve_top_matched_answers(questions,query):
    """
    Returns the top matched StackOverFlow Answers based on passed query and relevant Questions Extracted

    Parameters:
    questions (list): All Relevant questions extracted
    query (string) : Text Query whose answers are to be found

    Returns:
    list: 
        Type: Paragraph Object
        Description: Top Relevant StackOverFlow Answers (Sorted)

   """
    
    answer_list_list = []
    for question in questions:
        answer_list_list.append(get_answers_list(question['question']['id']))
    answer_obj_list = []
    for answer_list in answer_list_list:
        answer_obj_list.extend(process_answers(answer_list))

    answer_obj_list_sorted = sort_answers(answer_obj_list, query)
    answer_obj_list_sorted = answer_obj_list_sorted[:10]
    return answer_obj_list_sorted

def retrieve_top_matched_answer_paragraphs(questions, query):
     """
    Returns the top matched StackOverFlow Answer Paragraphs based on passed query and relevant Questions Extracted

    Parameters:
    questions (list): All Relevant questions extracted
    query (string) : Text Query whose answer summary is to be created

    Returns:
    list: 
        Type: Paragraph Object
        Description: Top Relevant StackOverFlow Answer Paragraphs(Sorted)

   """
    answer_list_list = []
    for question in questions:
        answer_list_list.append(get_answers_list(question['question']['id']))
    answer_obj_list = []
    for answer_list in answer_list_list:
        answer_obj_list.extend(process_answers_into_paragraphs(answer_list))

    answer_obj_list_sorted = sort_paragraphs(answer_obj_list, query)
    answer_obj_list_sorted = answer_obj_list_sorted[:10]
    return answer_obj_list_sorted

if __name__ == '__main__':
    pass