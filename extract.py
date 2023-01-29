from rule import SC
import numpy as np
from nltk.tokenize import sent_tokenize
import pandas as pd


noun_pos = ["NN", "NNS", "NNP"]
MR = ["amod", "advmod", "rcmod", "s", "subj", "obj", "nsubj"]
adj_pos = ["JJ", "JJS", "JJR"]


def preprocessing(text):
    text = text.lower()
    return text


def extract(review, aspect_dictionary):
    extracted = {}
    for aspect in aspect_dictionary:
        extracted[aspect] = []
    review = preprocessing(review)
    sentences = sent_tokenize(str(review))
    for sentence in sentences:
        tokenize, pos, dependency = SC(sentence)
        tokenize = np.array(tokenize)
        for index, i in enumerate(pos):
            if i[1] in noun_pos:
                for aspect in aspect_dictionary:
                    if i[1] in aspect_dictionary[aspect]:
                        for j in dependency:
                            if j[0] in MR:
                                if j[1] == (index + 1):
                                    relate_word_position = j[2]
                                    if pos[relate_word_position - 1][1] in adj_pos:
                                        o = tokenize[relate_word_position - 1]
                                        if o not in extracted[aspect]:
                                            extracted[aspect].append(o)

                                elif j[2] == (index + 1):
                                    relate_word_position = j[1]
                                    for j in dependency:
                                        if j[0] in MR:
                                            if j[2] != (index + 1) and j[1] == relate_word_position:
                                                relate_word_position = j[2]
                                                if pos[relate_word_position-1][1] in adj_pos:
                                                    o = tokenize[relate_word_position - 1]
                                                    if o not in extracted[aspect]:
                                                        extracted[aspect].append(o)
    return extracted


