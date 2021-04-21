"""
    Contains relevant methods for Inserting Data into Elastic Search Server

"""


from elasticsearch import Elasticsearch, helpers
import csv
import json
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

def csv_reader(file_obj, index_name):
    reader = csv.DictReader(file_obj)
    helpers.bulk(es, reader, index=index_name)


if __name__ == "__main__":
    with open("../Data/questions_data.csv") as f_obj:
        csv_reader(f_obj, "answerbot_questions")
    with open("../Data/answers_data.csv") as f_obj:
        csv_reader(f_obj, "answerbot_answers")
