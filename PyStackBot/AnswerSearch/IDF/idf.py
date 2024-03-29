"""
    Generates the text corpus from questions data, calculates the TFidf scores and generated an IDF.csv file.

"""


import csv
import sys
sys.path.append("./AnswerSearch/PreProcessor")
sys.path.append("./AnswerSearch/Data")
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from preprocessor import PreprocessPostContent


def get_corpus():
    pp_text = []
    dataset = pd.read_csv('../Data/questions_data.csv')

    print("dataset size:", len(dataset))
    cnt = 0

    for text in dataset['title']:
        pp_text_data = PreprocessPostContent().get_single_para_word_list(text)
        pp_text.append(pp_text_data)
        
        cnt += 1
        if cnt%10000 == 0:
            print(f"completed adding {cnt}/{len(dataset)} to corpus")

    return pp_text


def idf_vectorizer(corpus):
    vectorizer = TfidfVectorizer()
    vectorizer.fit(corpus)
    idf = vectorizer.idf_
    idf_dict = dict(zip(vectorizer.get_feature_names(), idf))
    return idf_dict


def to_csv(idf_dict, file_name="idf.csv"):
    with open(file_name, 'w', encoding="utf8") as f:
        f.write("Word, IDF\n") # header
        for key in idf_dict.keys():
            f.write("%s, %s\n" % (key, idf_dict[key]))

    print("successfully wrote data to the csv file.\n")

if __name__ == '__main__':
    corpus = get_corpus()
    print("successfully created corpus")
    idf_dict = idf_vectorizer(corpus)
    to_csv(idf_dict)