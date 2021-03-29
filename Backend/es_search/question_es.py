from elasticsearch import Elasticsearch


def search_question(query):
    # Query Passed by user
    size = 100
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

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
        index="answerbot_questions", body=doc, size=size)
    relevant_questions = []
    for res in returned_questions['hits']['hits']:
        relevant_questions.append(res['_source'])

    return relevant_questions


if __name__ == "__main__":
    query = "sort array in reverse"
    res = search_question(query)
    for q in res:
        print(q)
        print("\n\n")
    print(len(res))
