import sys
sys.path.append('./QuestionsRetrieval')
sys.path.append('./AnswersRetrieval')
from questionretrieval import retrieve_top_matched_questions
from answersretrieval import retrieve_top_matched_answers

while True:
    inp = input("query > ")
    if inp == "exit":
        break
    inp = inp.split("--")
    query = inp[0]
    questions = retrieve_top_matched_questions(query, 5, len(inp)>1)
    retrieve_top_matched_answers(questions, query)