
import sys
sys.path.append("../preprocessor")
sys.path.append("../es_search")


def custom_key(e):
    return e[1]


def retrieve_top_matched_questions(query, number_of_questions):
    from question_es import search_question
    from preprocessor import PreprocessPostContent
    questions = search_question(query)
    preprocessor = PreprocessPostContent()

    processed_question_titles = []

    for q in questions:
        processed_question_titles.append(
            preprocessor.get_single_para_word_list(q["title"]))

    preprocessed_query = preprocessor.get_single_para_word_list(query)

    relevance_scores = []
    # stores pair of questions and it's score

    for processed_q in processed_question_titles:
        pair = []
        pair.append(processed_q)
        #score=calculate_relevance_score(processed_q, preprocessed_query)
        score = 1  # temporary
        pair.append(score)
        relevance_scores.append(pair)

    relevance_scores.sort(reverse=True, key=custom_key)
    # sort the questions in descending order with respect to their scores

    final_questions_list = []

    # get top n(number_of_questions) questions
    for i in range(number_of_questions):
        if i >= len(relevance_scores):
            break

        final_questions_list.append(relevance_scores[i][0])

    return final_questions_list
