import csv
import pandas as pd
from nltk import sent_tokenize
import gensim


def top_target_frequeny(extracted_target_file, data_file):
    target_frequency = {}
    top_target = []
    f = open(extracted_target_file)
    list_target = [line.replace("\n", "") for line in f.readlines()]
    df = pd.read_csv(data_file)
    reviews = df["Reviews"].tolist()[:10]
    for review in reviews:
        number_of_words = len(review.split())
        if number_of_words > 2:
            sentences = sent_tokenize(str(review))
            for sentence in sentences:
                for word in list_target:
                    if word in sentence:
                        if target_frequency.get(word) is None:
                            target_frequency[word] = 1
                        else:
                            target_frequency[word] += 1
    print(target_frequency)

    for n in range(20):
        target = max(target_frequency, key=target_frequency.get)
        top_target.append(target)
        target_frequency.pop(target)
    print(top_target)
    return top_target


def expand_target(embeddings):

    model = gensim.models.KeyedVectors.load_word2vec_format(embeddings, binary=False)

    neighbors = list(model.similar_by_word("good", topn=10))
    print(neighbors)


embeddings = "word-embeddings/pruned.word2vec.txt"
expand_target(embeddings)
