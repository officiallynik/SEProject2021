import sys
sys.path.append("../preprocessor")
sys.path.append("../data")

from preprocessor import PreprocessPostContent
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def get_corpus():
    pp_text = []
    dataset = pd.read_csv('../data/questions_data.csv')
    
    for text in dataset['title']:
        # print(text)
        pp_text_data = PreprocessPostContent().get_single_para_word_list(text)
        # print(pp_text_data)
        pp_text.append(pp_text_data)
    
    for text in dataset['body']:
        pp_text_data = PreprocessPostContent().get_mul_para_wordlist_list(text)
        pp_text.append(pp_text_data)

    return pp_text

def idf_vectorizer(corpus):
    vectorizer = TfidfVectorizer()
    vectorizer.fit(corpus)
    idf = vectorizer.idf_
    idf_dict = dict(zip(vectorizer.get_feature_names(), idf))
    return idf_dict

def to_csv(idf_dict, file_name="idf.csv"):
    with open(file_name, 'w') as f:
        for key in idf_dict.keys():
            f.write("%s, %s\n" % (key, idf_dict[key]))

if __name__ == '__main__':
    corpus = get_corpus()
    # print(corpus)
    idf_dict = idf_vectorizer(corpus)
    to_csv(idf_dict)