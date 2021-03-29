# Maximal Marginal Relevance 

import sys
sys.path.append('../AnswersRetrieval')
from RCA import RCA
relevance = RCA()


class mmr_grid:
    # instances of this class holds relevance value of two paragraphs along with their positions

    def __init__(self,x,y):
        self.x=x
        self.y=y
       
    def __gt__(self,other):
        return self.mmr_val > other.mmr_val

    def calculate_relevance(self,sorted_paragraphs):
        self.mmr_val=relevance.calc_symmetric_relevance(sorted_paragraphs[x].word_list,sorted_paragraphs[y].word_list)