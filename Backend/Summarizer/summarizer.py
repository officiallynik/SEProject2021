# Given a list of paragraphs, returns a summarized version removing redundancy while maintaining novelty.
from mmr import mmr

def calculate_mmr_values(sorted_paragraphs):
    n=len(sorted_paragraphs)