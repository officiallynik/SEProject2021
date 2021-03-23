from elasticsearch import Elasticsearch, helpers
import csv
import json
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
print(es)


# def csv_reader_row_wise(file_obj, doc_name):
#     reader = csv.DictReader(file_obj)
#     i = 1

#     for row in reader:
#         print(i)
#         es.index(index='answerbot', doc_type=doc_name, id=i,
#                  body=json.dumps(row))
#         i = i + 1
#         # print(row)
#         if i == 500:
#             break


def csv_reader(file_obj, index_name, doc_name):
    reader = csv.DictReader(file_obj)
    helpers.bulk(es, reader, index=index_name, doc_type=doc_name)


if __name__ == "__main__":
    # with open("../Data/questions_data.csv") as f_obj:
    #     csv_reader(f_obj, "answerbot_questions", "questions")
    with open("../Data/answers_data.csv") as f_obj:
        csv_reader(f_obj, "answerbot_answers", "answers")
