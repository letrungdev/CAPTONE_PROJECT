from rule import SC
import numpy as np
from nltk.tokenize import sent_tokenize
import json


noun_pos = ["NN", "NNS", "NNP"]
MR = ["amod", "advmod", "rcmod", "s", "subj", "obj", "nsubj"]
adj_pos = ["JJ", "JJS", "JJR"]


def preprocessing(text):
    text = text.lower()
    return text


def extract(review, aspect_dictionary):
    extracted = {}
    f = open(aspect_dictionary)
    aspect_dictionary = json.load(f)
    for aspect in aspect_dictionary:
        extracted[aspect] = []
    review = preprocessing(review)

    sentences = sent_tokenize(str(review))
    for sentence in sentences:
        print(sentence)
        tokenize, pos, dependency = SC(sentence)
        tokenize = np.array(tokenize)
        for index, i in enumerate(pos):
            if i[1] in noun_pos:
                for aspect in aspect_dictionary:
                    if i[0] in aspect_dictionary[aspect]:
                        for j in dependency:
                            print(j)
                            if j[0] in MR:
                                if j[2] == (index + 1):
                                    relate_word_position = j[1]
                                    if pos[relate_word_position - 1][1] in adj_pos:
                                        o = tokenize[relate_word_position - 1]
                                        if o not in extracted[aspect]:
                                            extracted[aspect].append(o)
    return extracted


