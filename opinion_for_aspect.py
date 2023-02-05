from rule import SC
import numpy as np
from nltk.tokenize import sent_tokenize
from preprocessing import preprocessing
import json


noun_pos = ["NN", "NNS", "NNP"]
MR = ["amod", "advmod", "rcmod", "s", "subj", "obj", "nsubj"]
adj_pos = ["JJ", "JJS", "JJR"]


def opinion_for_aspect(reviews, aspect_dictionary):
    opinion_for_aspect = {}
    f = open(aspect_dictionary)
    aspect_dictionary = json.load(f)
    for aspect in aspect_dictionary:
        opinion_for_aspect[aspect] = []

    for review in reviews:
        review = preprocessing(review)
        if len(review.split()) > 1:
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
                                    if j[0] in MR:
                                        if j[2] == (index + 1):
                                            relate_word_position = j[1]
                                            if pos[relate_word_position - 1][1] in adj_pos:
                                                print(j)
                                                o = tokenize[relate_word_position - 1]
                                                if o not in opinion_for_aspect[aspect]:
                                                    print(o)
                                                    opinion_for_aspect[aspect].append(o)
                                        elif j[1] == (index + 1):
                                            relate_word_position = j[2]
                                            if pos[relate_word_position - 1][1] in adj_pos:
                                                print(j)
                                                o = tokenize[relate_word_position - 1]
                                                if o not in opinion_for_aspect[aspect]:
                                                    print(o)
                                                    opinion_for_aspect[aspect].append(o)

    with open('opinion_for_aspect.json', 'w') as fp:
        json.dump(opinion_for_aspect, fp, indent=4, ensure_ascii=False)
    return opinion_for_aspect