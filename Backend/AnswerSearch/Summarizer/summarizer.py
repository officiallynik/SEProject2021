"""

Given a list of paragraphs, returns a summarized version removing redundancy while maintaining novelty.

"""
from mmr import mmr
import sys
sys.path.append('./AnswerSearch/QuestionRetrieval')
from RCA import RCA
relevance = RCA()

class mmr_handler:
    """ 
        Contains relevant methods for Maximal Marginal Relevance (MMR) Calculation.
    """
    def build_mmr_matrix(self,sorted_paragraphs):
        """
        Returns MMR Matrix
        
        Parameters:
        sorted_paragraphs (list)
       

        Returns:
        2D List: MMR Matrix
            
        """
        n=len(sorted_paragraphs)

        mmr_matrix = [[0.0 for i in range(n)] for j in range(n)]

        for i in range(len(sorted_paragraphs)):
            for j in range(len(sorted_paragraphs)):
                if(i == j):
                    mmr_matrix[i][j] = 0.0
                else:
                    mmr_matrix[i][j] = relevance.calc_symmetric_relevance(
                        sorted_paragraphs[i].word_list, sorted_paragraphs[j].word_list)
                    

        return mmr_matrix


    def rank_mmr(self,sorted_paragraphs):
        """
        Sorts the passed paragraphs based on MMR scores and returns the top 5 paragraphs.
        
        Parameters:
        sorted_paragraphs (list)
       

        Returns:
        List: Paragraphs sorted based on MMR scores
            
        """
        mmr_matrix = self.build_mmr_matrix(sorted_paragraphs)
        
        final_paragraphs = []

        para_ranked = []
        para_unranked = [i for i in range(len(sorted_paragraphs))]
        lambda_=0.5

        for i in range(len(sorted_paragraphs)):
            max_mmr_val = -sys.float_info.max
            max_mmr_index = None

            for r in para_unranked:
                max_sim = -sys.float_info.max

                for s in para_ranked:
                    if mmr_matrix[r][s] > max_sim:
                        max_sim = mmr_matrix[r][s]
                    
                mmr_val=sorted_paragraphs[r].relevance_score*lambda_ - (1-lambda_)*max_sim

                if mmr_val>max_mmr_val:
                    max_mmr_val=mmr_val
                    max_mmr_index=r

            final_paragraphs.append({"mmr_score":max_mmr_val, "mmr_index":max_mmr_index, "paragraph":sorted_paragraphs[max_mmr_index]})           
            para_unranked.remove(max_mmr_index)
            para_ranked.append(max_mmr_index)
        
       

        return final_paragraphs[:5]

    
