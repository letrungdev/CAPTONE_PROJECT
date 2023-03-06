from stanfordcorenlp import StanfordCoreNLP
import numpy as np
import requests
from bs4 import BeautifulSoup
import multiprocessing as mp
import json

corenlp_path = "stanford-corenlp-4.5.1"

MR = ["amod", "advmod", "rcmod", "s", "subj", "obj", "nsubj"]
noun_pos = ["NN", "NNS", "NNP"]
adj_pos = ["JJ", "JJS", "JJR"]


compound_noun_pattern = {
    1: ("JJ", "NN"),
    2: ("JJ", "NNS"),
    3: ("NN", "NN"),
    4: ("VB", "RP")
}


def SC(text):
    nlp = StanfordCoreNLP(corenlp_path)
    tokenize = nlp.word_tokenize(text)
    pos = nlp.pos_tag(text)
    dependency = nlp.dependency_parse(text)
    nlp.close()
    return tokenize, pos, dependency


def modify_noun_pos(pos_tags):
    if len(pos_tags) > 1:
        temp_pos = pos_tags.copy()
        try:
            for index, pos in enumerate(temp_pos[:-1]):
                for pattern in compound_noun_pattern:
                    if compound_noun_pattern[pattern][0] == pos[1]:
                        next_word = temp_pos[index+1]
                        if compound_noun_pattern[pattern][1] == next_word[1]:
                            compound_word = pos[0] + " " + next_word[0]
                            # request wikipedia, if word in wikipedia
                            url = "https://en.wikipedia.org/wiki/{}"
                            page = requests.get(url.format(compound_word))
                            soup = BeautifulSoup(page.text, "html.parser")
                            a = soup.find(class_="vector-pinnable-header-label")
                            if a is not None:
                                pos_tags[index] = list(pos_tags[index])
                                pos_tags[index][0] = compound_word
                                pos_tags[index][1] = "NN"
                                pos_tags[index] = tuple(pos_tags[index])
                                del pos_tags[index+1]
        except:
            pass
    return pos_tags


def extract_target_rule(text, opinion_words):
    list_target = []
    tokenize, pos, dependency = SC(text)
    compound_modify = modify_noun_pos(pos.copy())
    if compound_modify == pos:
        tokenize = np.array(tokenize)
        for index, i in enumerate(pos):
            if i[1] in adj_pos and i[0] in opinion_words:
                for j in dependency:
                    if j[0] in MR:
                        try:
                            if j[2] == (index + 1):
                                relate_word_position = j[1]
                                if pos[relate_word_position - 1][1] in noun_pos:
                                    t = tokenize[relate_word_position - 1]
                                    list_target.append(t)
                            elif j[1] == (index + 1):
                                relate_word_position = j[2]
                                if pos[relate_word_position - 1][1] in noun_pos:
                                    t = tokenize[relate_word_position - 1]
                                    list_target.append(t)
                        except:
                            pass
    else:
        for pos in compound_modify:
            if pos[1] in noun_pos:
                list_target.append(pos[0])

    list_target = list(set(list_target))
    return list_target


def extract_target_opinion_rule(text, target_dictionary):
    aspect_opinion = {}
    tokenize, pos, dependency = SC(text)
    tokenize = np.array(tokenize)
    compound_modify = modify_noun_pos(pos.copy())
    for aspect in target_dictionary:
        if compound_modify == pos:
            for index, i in enumerate(pos):
                if i[0] in target_dictionary[aspect] and i[1] in noun_pos:
                    for j in dependency:
                        if j[2] == (index + 1) and j[0] in MR:
                            relate_word_position = j[1]
                            try:
                                if pos[relate_word_position - 1][1] in adj_pos:
                                    t = tokenize[relate_word_position - 1]
                                    aspect_opinion[aspect] = t
                            except:
                                pass
                        elif j[1] == (index + 1) and j[0] in MR:
                            relate_word_position = j[2]
                            if pos[relate_word_position - 1][1] in adj_pos:
                                t = tokenize[relate_word_position - 1]
                                aspect_opinion[aspect] = t
        else:
            for index, i in compound_modify:
                if i[0] in target_dictionary[aspect] and i[1] in noun_pos:
                    try:
                        for n in range(5):
                            if compound_modify[index-1+n][1] in adj_pos:
                                aspect_opinion[aspect] = compound_modify[index-1+n][0]
                    except:
                        pass
    return aspect_opinion


def extract_target_polarity_rule(review, dictionary_file):
    aspect_polarity = {}
    with open(dictionary_file) as f:
        dictionary = json.load(f)
    tokenize, pos, dependency = SC(review)
    tokenize = np.array(tokenize)
    compound_modify = modify_noun_pos(pos.copy())
    for aspect in dictionary:
        if compound_modify == pos:
            for index, i in enumerate(pos):
                if i[0] in dictionary[aspect]["name"] and i[1] in noun_pos:
                    for j in dependency:
                        if j[2] == (index + 1) and j[0] in MR:
                            relate_word_position = j[1]
                            try:
                                if pos[relate_word_position - 1][1] in adj_pos:
                                    sentiment_word = tokenize[relate_word_position - 1]
                                    if sentiment_word in dictionary[aspect]['opinion']['neutral']:
                                        aspect_polarity[aspect] = 'neutral'
                                    elif sentiment_word in dictionary[aspect]['opinion']['negative']:
                                        aspect_polarity[aspect] = 'negative'
                                    else:
                                        aspect_polarity[aspect] = 'positive'
                            except:
                                pass
                        elif j[1] == (index + 1) and j[0] in MR:
                            relate_word_position = j[2]
                            if pos[relate_word_position - 1][1] in adj_pos:
                                sentiment_word = tokenize[relate_word_position - 1]
                                if sentiment_word in dictionary[aspect]['opinion']['neutral']:
                                    aspect_polarity[aspect] = 'neutral'
                                elif sentiment_word in dictionary[aspect]['opinion']['negative']:
                                    aspect_polarity[aspect] = 'negative'
                                else:
                                    aspect_polarity[aspect] = 'positive'
        else:
            for index, i in compound_modify:
                if i[0] in dictionary[aspect]["name"] and i[1] in noun_pos:
                    try:
                        for n in range(5):
                            if compound_modify[index - 2 + n][1] in adj_pos:
                                sentiment_word = compound_modify[index - 2 + n][0]
                                if sentiment_word in dictionary[aspect]['opinion']['neutral']:
                                    aspect_polarity[aspect] = 'neutral'
                                elif sentiment_word in dictionary[aspect]['opinion']['negative']:
                                    aspect_polarity[aspect] = 'negative'
                                else:
                                    aspect_polarity[aspect] = 'positive'
                    except:
                        pass
    return aspect_polarity

