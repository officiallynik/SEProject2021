"""

Contains relevant methods for building the text corpus from questions dataset

"""

import sys
sys.path.append("../PreProcessor")
sys.path.append("../Data")
import pandas as pd
from preprocessor import PreprocessPostContent

def process_data(data):
    preprocessor = PreprocessPostContent()
    title = preprocessor.get_single_para_word_list(data[0])
    body = preprocessor.get_mul_para_wordlist_list(data[1])
    
    return title, body

def create_corpus():
    dataset = pd.read_csv("../Data/questions_data.csv")

    for i in range(50000, 300000, 10000):
        datasubset = zip(dataset[i:i+10000]['title'], dataset[i:i+10000]['body'])

        data_list = []
        print("starting to process dataset")
        for data in datasubset:
            data_list.append(process_data(data))

        print("starting to add data to txt file")

        with open("corpus.txt", 'a', encoding="utf-8") as f:
            for data in data_list:
                f.write(f"{data[0]}\n{data[1]}\n")

        print(f"successfully wrote data to the csv file, completed: {i+10000} data items in total")

if __name__ == '__main__':
    create_corpus()