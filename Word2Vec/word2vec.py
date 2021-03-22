import sys
from gensim.models.word2vec import Word2Vec, LineSentence

def create_model(sentences):
    num_features = 1000  # dim
    min_word_count = 1  #
    num_workers = 40  # thread
    context = 10  # Context window size

    # Initialize and train the model (this will take some time)
    model = Word2Vec(sentences, workers=num_workers, size=num_features, min_count=min_word_count,
                     window=context)

    # save bin file(about 3G), and using KeyedVectors.load_word2vec_format("w2v_model.bin", binary=True) load later
    model.wv.save_word2vec_format("w2v_model.bin", binary=True)
    return model

if __name__ == '__main__':
    corpus_file = "./corpus.txt"
    print("building word2vec model")
    sentences = LineSentence(corpus_file)
    model = create_model(sentences)
    print("successfully built word2vec model")