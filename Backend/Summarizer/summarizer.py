# Given a list of paragraphs, returns a summarized version removing redundancy while maintaining novelty.
from mmr import mmr

def calculate_mmr_values(sorted_paragraphs):
    n=len(sorted_paragraphs)
    mmr_objects=[]
    try:
        for i in range(n):
            for j in range(i+1,n):
                mmr_obj=mmr(i,j)
                mmr_obj.calculate_relevance(sorted_paragraphs)
                mmr_objects.push(mmr_obj)
    except:
        print("error in "+str(i)+", "+str(j))
    
    return mmr_objects

def get_top_k_paragraphs(k,mmr_obj_list,sorted_paragraphs):
    
    mmr_obj_list.sort(reverse=True)

    top_paragraphs_indices=set()
    for i in range(len(mmr_obj_list)):
        top_paragraphs_indices.add(mmr_obj_list[i].x)
        top_paragraphs_indices.add(mmr_obj_list[i].y)
        if len(top_paragraphs_indices)>=k:
            break
    
    return top_paragraphs_indices

