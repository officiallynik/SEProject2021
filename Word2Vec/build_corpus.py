import multiprocessing as mp
import sys
sys.path.append("../PreProcessor")
sys.path.append("../Data")
import pandas as pd
from preprocessor import PreprocessPostContent

def process_data(data, cnt):
    preprocessor = PreprocessPostContent()
    title = preprocessor.get_single_para_word_list(data[0])
    body = preprocessor.get_mul_para_wordlist_list(data[1])
    
    if (cnt + 1)%10000 == 0:
        print(f"processed: {cnt} data items")
    
    return title, body

def create_corpus():
    dataset = pd.read_csv("../Data/questions_data.csv")
    dataset = zip(dataset[:10]['title'], dataset[:10]['body'])

    pool = mp.Pool(mp.cpu_count())

    print("starting to process dataset")
    data_list = [pool.apply(process_data, args=(data, cnt)) for cnt, data in enumerate(dataset)]
    # print(data_list)

    print("starting to add data to txt file")

    with open("corpus.txt", 'w', encoding="utf-8") as f:
        for data in data_list:
            f.write(f"{data[0]}\n{data[1]}\n")

    print("successfully wrote data to the csv file")

if __name__ == '__main__':
    create_corpus()