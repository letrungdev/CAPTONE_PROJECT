from nltk.corpus import wordnet
import pandas as pd
from nltk import sent_tokenize
import gensim
from collections import Counter
from difflib import SequenceMatcher


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def extracted_target(extracted_target_file, stop_words_file):
    f = open(extracted_target_file)
    g = open(stop_words_file)
    extracted_target = list(set([line.replace("\n", "") for line in f.readlines()]))
    stop_word = [line.replace("\n", "") for line in g.readlines()]
    targets = list((Counter(extracted_target)-Counter(stop_word)).elements())
    return list(set(targets))


def top_target(extracted_target, data_file):
    target_frequency = {}
    top_target = []
    df = pd.read_csv(data_file)
    reviews = df["Reviews"].tolist()[:10]
    for review in reviews:
        number_of_words = len(review.split())
        if number_of_words > 2:
            sentences = sent_tokenize(str(review))
            for sentence in sentences:
                for word in extracted_target:
                    if word in sentence:
                        if target_frequency.get(word) is None:
                            target_frequency[word] = 1
                        else:
                            target_frequency[word] += 1

    for n in range(10):
        target = max(target_frequency, key=target_frequency.get)
        try:
            top_target.append(target)
            target_frequency.pop(target)
        except:
            pass
    return top_target


def expand_target(extracted_target, top_target, embeddings):
    target_expand = {}
    other_target = list((Counter(extracted_target)-Counter(top_target)).elements())
    model = gensim.models.KeyedVectors.load_word2vec_format(embeddings, binary=False)
    for word in top_target:
        target_expand[word] = [word]

    # expand by similarity from word2vec
    for word in top_target:
        try:
            neighbors = list(model.similar_by_word(word, topn=10))
            if len(neighbors) > 0:
                for neighbor in neighbors:
                    if neighbor[0] in other_target:
                        print(neighbor[0])
                        target_expand[word].append(neighbor[0])
        except:
            pass

        for w in other_target:
            a = similar(word, w)
            if a > 0.8 and w not in target_expand[word]:
                target_expand[word].append(w)

    return target_expand


def prunning(review_file, extracted_target_file, stop_word_file, embeddings):
    targets = extracted_target(extracted_target_file, stop_word_file)
    top = top_target(targets, review_file)
    print(top)
    expand = expand_target(extracted_target, top, embeddings)
    print(expand)
    return expand



