import sys
sys.path.append('./AnswerSearch/IDF')
import csv
from RCA import RCA
relevance = RCA()

class Paragraph():
    """
    Entity of this class is either an entire answer or an answer paragraph

   """
    def __init__(self, raw_text, word_list, vote_score, position):
        self.raw_text = raw_text # contains original paragraph text
        self.word_list = word_list # contains tokenized paragraph words list
        self.position = position # relative position of the paragraph in the answer
        self.vote_score = vote_score # Votes received by answer on StackOverFlow
        self.relevance_score = 0 # Relevance score of paragraph with respect to the user query 
        self.entity_score = 0 # Entity score of paragraph 
        self.infor_entropy = 0 # Information Entropy of paragraph 
        self.semantic_pattern = 0 # If an answer paragraph contains at least one of the sentence patterns, then paragraph’s pattern value is 1, otherwise 0.
        self.format_pattern = 0 # If an answer paragraph contains specific HTML tags, its format pattern score is 1, otherwise 0.
        self.pos_score = 0 # position score. Position Score = 1/position
        self.overall_score = 0 # Overall Score of the paragraph
        self.idf_metric_dict = self.get_idf_metrics()

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

    def cal_relevance(self, query_word_list):
        """
        Calculates relevance score of paragraph with respect to the User Query
        
        Parameters:
        query_word_list (list): Tokenized User Query

        Returns:
        None
            
        """
        self.relevance_score = relevance.calc_symmetric_relevance(query_word_list, self.word_list)

    def cal_entropy(self):
        """
        Calculates Entropy score of paragraph
        
        Parameters:
        None

        Returns:
        None
            
        """
        idf_list = []
        for word in self.word_list:
            try:
                idf = self.idf_metric_dict[word]
            except:
                idf = 0

            idf_list.append(idf)

        self.infor_entropy = sum(idf_list)

    def cal_semantic_pattern(self):
        """
        Finds whether any pattern string is found in the paragraph
        
        Parameters:
        None

        Returns:
        None
            
        """


        pattern = ['please check', 'pls check', 'you should',
                   'you can try', 'you could try', 'check out',
                   'in short', 'the most important', 'i\'d recommend',
                   'in summary', 'keep in mind', 'i suggest']

        lower_plain_text = self.raw_text.lower()

        for p in pattern:
            if lower_plain_text.find(p) != -1:
                self.semantic_pattern = 1
                break

    def cal_format_pattern(self):
        """
        Finds whether any pattern string is found in the paragraph
        
        Parameters:
        None

        Returns:
        None
            
        """
        pattern = ['<strong>', '<strike>']

        lower_plain_text = self.raw_text.lower()

        for p in pattern:
            if lower_plain_text.find(p) != -1:
                self.format_pattern = 1
                break

    def normalized(self, relevance_min, relevance_max, entropy_min, entropy_max, vote_min, vote_max):
        """
        Normalizes all scores
        
        Parameters:
        relevance_min (int): minimum relevance value among all answer paragraphs
        relevance_max (int): maximum relevance value among all answer paragraphs
        entropy_min   (int): minimum entropy value among all answer paragraphs
        entropy_max   (int): maximum entropy value among all answer paragraphs
        vote_min      (int): minimum votes among all answer paragraphs
        vote_max      (int): maximum votes among all answer paragraphs

        Returns:
        None
            
        """
        if relevance_max - relevance_min != 0:
            self.relevance_score = (self.relevance_score - relevance_min) / (relevance_max - relevance_min)
        else:
            self.relevance_score = self.relevance_score - relevance_min
            
        if entropy_max - entropy_min != 0:
            self.infor_entropy = (self.infor_entropy - entropy_min) / (entropy_max - entropy_min)
        else:
            self.infor_entropy = self.infor_entropy - entropy_min
            
        if vote_max - vote_min != 0:
            self.vote_score = (self.vote_score - vote_min) / (vote_max - vote_min)
        else:
            self.vote_score = self.vote_score - vote_min
        
    def cal_overall_score(self):
        """
        Calculates the overall score by summing up all the score
        
        Parameters:
        None

        Returns:
        None
            
        """
        self.overall_score += self.vote_score
        self.overall_score += self.relevance_score
        self.overall_score += self.entity_score
        self.overall_score += self.infor_entropy
        self.overall_score += self.semantic_pattern
        self.overall_score += self.format_pattern
        self.overall_score += self.pos_score

    def __gt__(self, other):
        """
            Operator Overloading. Used for sorting the answer paragraphs based on overall score.
        """
        return self.overall_score > other.overall_score


        