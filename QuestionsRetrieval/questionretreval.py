import sys
sys.path.append("../PreProcessor")
sys.path.append("../es_search")
from question_es import search_question
from preprocessor import PreprocessPostContent
from RCA import RCA


def custom_key(e):
    return e['score']


def retrieve_top_matched_questions(query, number_of_questions):

    relevance_calculator = RCA()
    questions = search_question(query)
    preprocessor = PreprocessPostContent()

    processed_question_titles = []

    for q in questions:
        processed_question_titles.append(
            {
                'id': q["id"], 
                'title': preprocessor.get_single_para_word_list(q["title"])
            }
        )

    # (processed_question_titles)

    preprocessed_query = preprocessor.get_single_para_word_list(query)

    relevance_scores = []
    # stores dict of questions and it's score

    for processed_q in processed_question_titles:
        score = relevance_calculator.calc_symmetric_relevance(
            preprocessed_query, processed_q['title'])
        relevance_scores.append({'score': score, 'question': processed_q})

    # print(relevance_scores)

    relevance_scores.sort(reverse=True, key=custom_key)
    # sort the questions in descending order with respect to their scores

    # print(relevance_scores)

    final_questions_list = []

    # get top n(number_of_questions) questions
    for i in range(number_of_questions):
        if i >= len(relevance_scores):
            break

        final_questions_list.append(relevance_scores[i]['question'])

    return final_questions_list


if __name__ == "__main__":
    query = "sort array in reverse"

    print(retrieve_top_matched_questions(query, 5))
