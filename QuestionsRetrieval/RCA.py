import csv
import sys
sys.path.append("../IDF")
sys.path.append("../Word2Vec")
from idf import from_csv
from gensim.models import Word2Vec


class RCA:
    def get_idf_metrics(self):
        idf_metric_dict = from_csv()

    def get_word2vec_model(self):
        print("loading word2vec model")
        model = Word2Vec.load("../Word2Vec/word2vec.bin")
        print("model loaded successfully")
        return model

    def __init__(self):
        self.idf_dict = self.get_idf_metrics()
        self.word2Vec = self.get_word2vec_model()

    def calc_asymmetric_val(self, query_list, Question_List):
        rel_idf_summation = []
        idf_values = []

        for query in query_list:

            total_rel = []
            for question in Question_List:
                try:
                    rel = self.word2Vec.similarity(query, question)
                except Exception as e:
                    rel = 0
                total_rel.append(rel)
            try:
                idf_val = self.idf_dict[query]
                idf = float(idf_val)

            except:
                idf = 0
            total_rel.append(0)
            max_rel = max(total_rel)
            rel_idf_summation.append(max_rel * idf)
            idf_values.append(idf)

        idf_summation = sum(idf_values)

        if idf_summation != 0:
            asymmetric_rel = sum(rel_idf_summation) / idf_summation
        else:
            asymmetric_rel = 0

        return asymmetric_rel

    def calc_symmetric_relevance(self, query_list, Question_List):
        rel_q_to_Q = self.calc_asymmetric_val(query_list, Question_List)
        rel_Q_to_q = self.calc_asymmetric_val(Question_List, query_list)
        average_relevance = (rel_q_to_Q + rel_Q_to_q) / 2
        return average_relevance

if __name__ == "__main__":
    pass