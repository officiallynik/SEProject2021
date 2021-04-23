import csv
import sys
sys.path.append("./AnswerSearch/IDF")
sys.path.append("./AnswerSearch/Word2Vec")
from gensim.models import Word2Vec


class RCA:
    """
    Contains relevant methods for relevance calculation

    """
    def get_idf_metrics(self):
        """
        Returns a dictionary of words with their idf scores.
        
        Parameters:
        None

        Returns:
        Dictionary: words with their idf scores
            
        """
        idf_metric_dict = {}
        with open("./AnswerSearch/IDF/idf.csv", encoding="utf8") as f:
            read_csv = csv.reader(f, delimiter=',')
           
            for row in read_csv:
                idf_metric_dict[row[0]] = row[1]
        return idf_metric_dict

    def get_word2vec_model(self):
        """
        Returns the trained Word2Vec Model 

        Parameters:
        None

        Returns:
        Trained Model
            
        """
        model = Word2Vec.load("./AnswerSearch/Word2Vec/word2vec.model")
        self.word_vectors = model.wv
        return model

    def __init__(self):
        self.idf_dict = self.get_idf_metrics()
        self.word2Vec = self.get_word2vec_model()


    def calc_asymmetric_val(self, query_list, Question_List):
        """
        Returns the calculated asymmetric relevance score between passed query_list and Question_list
        
        Parameters:
        query_list, Question_List (list): List of words 

        Returns:
        float: relevance score
            
        """
        rel_idf_summation = []
        idf_values = []

        for query in query_list:

            total_rel = []
            for question in Question_List:
                try:
                    
                    rel = self.word_vectors.similarity(w1=query,w2=question)
                except Exception as e:
                    
                    rel = 0
                
                total_rel.append(rel)
            try:
                idf_val = self.idf_dict[query]
                idf = float(idf_val)
            except Exception as e:
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
        """
        Returns the calculated symmetric relevance score between passed query_list and Question_list
        
        Parameters:
        query_list, Question_List (list): List of words 

        Returns:
        float: relevance score
            
        """
       
        rel_q_to_Q = self.calc_asymmetric_val(query_list, Question_List)
        rel_Q_to_q = self.calc_asymmetric_val(Question_List, query_list)
        average_relevance = (rel_q_to_Q + rel_Q_to_q) / 2
        
        return average_relevance

if __name__ == "__main__":
    rca = RCA()
    rca.get_word2vec_model()