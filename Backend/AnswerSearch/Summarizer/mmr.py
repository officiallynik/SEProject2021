# Maximal Marginal Relevance

from RCA import RCA
import sys
sys.path.append('./AnswerSearch/QuestionsRetrieval')
relevance = RCA()


class mmr:
    # instances of this class holds relevance row of a paragraph

    def __init__(self, x):
        self.x = x

    # def __gt__(self,other):
    #     return self.mmr_val > other.mmr_val

    def calculate_relevance(self, sorted_paragraphs):
        mmr_values = [0 for i in range(len(sorted_paragraphs))]
        for i in range(len(sorted_paragraphs)):
            if i == self.x:
                mmr_values[i] = 0.0
            else:
                mmr_values[i] = relevance.calc_symmetric_relevance(
                    sorted_paragraphs[self.x].word_list, sorted_paragraphs[i].word_list)

        self.mmr_values = mmr_values
