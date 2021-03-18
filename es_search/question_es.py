from elasticsearch import Elasticsearch


def search_question(query):
    # Query Passed by user
    size = 1000
    url = "http://localhost:9200"

    es = Elasticsearch([url])

    doc = {
        "query": {
            "bool": {
                "should": [
                    {"match": {"title": query}}
                ]
            }
        }
    }
    returned_questions = es.search(
        index="questions", doc_type="", body=doc, size=size)
    relevant_questions = []
    for res in returned_questions['hits']['hits']:
        relevant_questions.append(res['_source'])

    return relevant_questions
