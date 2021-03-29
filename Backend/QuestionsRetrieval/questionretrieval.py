import sys
sys.path.append("./PreProcessor")
sys.path.append("./es_search")
from question_es import search_question
from preprocessor import PreprocessPostContent
from RCA import RCA
import nltk

def custom_key(e):
    return e['score']

def questions_display(questions, display=False):
    if display:
        for cnt, question in enumerate(questions, 1):
            print('question no.:', cnt)
            print('question:', question['question']['title'])
            print()

def retrieve_top_matched_questions(query, number_of_questions, display):

    relevance_calculator = RCA()
    questions = search_question(query)
    preprocessor = PreprocessPostContent()

    processed_question_titles = []

    # print("number of questions:", len(questions))

    for q in questions:
        processed_question_titles.append(
            {
                'id': q["id"], 
                'title': preprocessor.get_single_para_word_list(q["title"])
            }
        )

    # print(processed_question_titles)

    preprocessed_query = preprocessor.get_single_para_word_list(query)
    query_tokens = nltk.word_tokenize(preprocessed_query)
    # print(query_tokens)

    relevance_questions = []
    # stores dict of questions and it's score

    for processed_q in processed_question_titles:
        question_tokens = nltk.word_tokenize(processed_q['title'])
        score = relevance_calculator.calc_symmetric_relevance(query_tokens, question_tokens)
        # print(question_tokens, score)
        relevance_questions.append({'score': score, 'question': processed_q})

    # print(relevance_questions)

    relevance_questions.sort(reverse=True, key=custom_key)
    # sort the questions in descending order with respect to their scores

    questions_display(relevance_questions[:number_of_questions], display)

    return relevance_questions[:number_of_questions]

if __name__ == "__main__":
    query = "sort array in reverse"

    retrieve_top_matched_questions(query, 10, True)
