import sys
sys.path.append('./IDF')
import csv
from RCA import RCA
relevance = RCA()

class Paragraph():
    def __init__(self, raw_text, word_list, vote_score, position):
        self.raw_text = raw_text
        self.word_list = word_list
        self.position = position
        self.vote_score = vote_score
        self.relevance_score = 0
        self.entity_score = 0
        self.infor_entropy = 0
        self.semantic_pattern = 0
        self.format_pattern = 0
        self.pos_score = 0
        self.overall_score = 0
        self.idf_metric_dict = self.get_idf_metrics()

    def get_idf_metrics(self):
        idf_metric_dict = {}
        with open("./IDF/idf.csv", encoding="utf8") as f:
            read_csv = csv.reader(f, delimiter=',')
            # print("loading idf metrics")
            for row in read_csv:
                idf_metric_dict[row[0]] = row[1]

        return idf_metric_dict

    def cal_relevance(self, query_word_list):
        self.relevance_score = relevance.calc_symmetric_relevance(query_word_list, self.word_list)

    def cal_entropy(self):
        idf_list = []
        for word in self.word_list:
            try:
                idf = self.idf_metric_dict[word]
            except:
                idf = 0

            idf_list.append(idf)

        self.infor_entropy = sum(idf_list)

    def cal_semantic_pattern(self):
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
        pattern = ['<strong>', '<strike>']

        lower_plain_text = self.raw_text.lower()

        for p in pattern:
            if lower_plain_text.find(p) != -1:
                self.format_pattern = 1
                break

    # def cal_pos_score(self):
    #     if self.position >= 1 and self.position <= 3:
    #         self.pos_score = 1 / self.position
    #     else:
    #         self.pos_score = 0

    def normalized(self, relevance_min, relevance_max, entropy_min, entropy_max, vote_min, vote_max):
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
        #print(self.vote_score, self.relevance_score, self.entity_score, self.infor_entropy, self.semantic_pattern, self.format_pattern)
        self.overall_score += self.vote_score
        self.overall_score += self.relevance_score
        self.overall_score += self.entity_score
        self.overall_score += self.infor_entropy
        self.overall_score += self.semantic_pattern
        self.overall_score += self.format_pattern
        self.overall_score += self.pos_score

    def __gt__(self, other):
        return self.overall_score > other.overall_score


        