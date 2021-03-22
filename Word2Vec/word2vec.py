import sys
sys.path.append("../preprocessor")
sys.path.append("../data")
import pandas as pd
from multiprocessing import Pool
from gensim.models import Word2Vec
from preprocessor import PreprocessPostContent


def process(post_bulk):
    wordlist_list = []
    preprocessor = PreprocessPostContent()
    for post in post_bulk:
        wordlist_list.append(preprocessor.get_single_para_word_list(post[0]))
        wordlist_list.extend(preprocessor.get_mul_para_wordlist_list(post[1]))

    return wordlist_list


def parallel_process(posts):
    bulk = []
    block_list = []
    count = 0
    pool = Pool(50)
    for post in posts:
        bulk.append(post)
        count += 1
        if not count % 2:
            block_list.append(bulk)
            bulk = []
        if count == 4:
            break

    block_list.append(bulk)
    return_list = pool.map(process, block_list)
    pool.close()
    pool.join()
    return return_list

def create_corpus():
    dataset = pd.read_csv("../data/questions_data.csv")
    return_list = parallel_process(zip(dataset['title'], dataset['body']))
    corpus_wordlist_list = []

    for ls in return_list:
        corpus_wordlist_list.extend(ls)

    return corpus_wordlist_list


def create_model(corpus_wordlist_list):
    num_features = 1000  # dim
    min_word_count = 1  #
    num_workers = 40  # thread
    context = 10  # Context window size

    # Initialize and train the model (this will take some time)
    model = Word2Vec(corpus_wordlist_list, workers=num_workers, size=num_features, min_count=min_word_count,
                     window=context)

    # save bin file(about 3G), and using KeyedVectors.load_word2vec_format("w2v_model.bin", binary=True) load later
    model.wv.save_word2vec_format("w2v_model.bin", binary=True)
    return model

if __name__ == '__main__':
    corpus_wordlist_list = create_corpus()
    model = create_model(corpus_wordlist_list)