from stanfordcorenlp import StanfordCoreNLP
import numpy as np
import logging


corenlp_path = "stanford-corenlp-4.5.1"
modifiers = ["amod", "advmod", "rcmod", "pnmod"]
MR = ["amod", "advmod", "rcmod", "s", "subj", "obj", "nsubj"]
noun_pos = ["NN", "NNS", "NNP"]
adj_pos = ["JJ", "JJS", "JJR"]


def SC(text):
    nlp = StanfordCoreNLP(corenlp_path)
    tokenize = nlp.word_tokenize(text)
    pos = nlp.pos_tag(text)
    dependency = nlp.dependency_parse(text)
    nlp.close()
    return tokenize, pos, dependency


def rule1(text, opinion_file):
    list_target = []
    tokenize, pos, dependency = SC(text)
    tokenize = np.array(tokenize)
    for index, i in enumerate(pos):
        if i[1] in adj_pos:
            # NOTE
            with open(opinion_file) as f:
                if i[0] in f.read():
                    f.close()
                    for j in dependency:
                        if j[2] == (index + 1) and j[0] in MR:
                            relate_word_position = j[1]
                            if pos[relate_word_position-1][1] in noun_pos:
                                t = tokenize[relate_word_position-1]
                                list_target.append(t)
                                # O-->O-dep-->T
                            for j in dependency:
                                if j[0] in MR:
                                    if j[1] == relate_word_position:
                                        relate_word_position = j[2]
                                        if pos[relate_word_position-1][1] in noun_pos:
                                            t = tokenize[relate_word_position-1]
                                            list_target.append(t)
                                            # O-->O-dep-->H<--T-dep<--T

    list_target = list(set(list_target))
    return list_target


def rule2(text, target_file):
    list_opinion = []
    tokenize, pos, dependency = SC(text)
    tokenize = np.array(tokenize)
    for index, i in enumerate(pos):
        if i[1] in noun_pos:
            with open(target_file) as f:
                if i[0] in f.read():
                    f.close()
                    for j in dependency:
                        if j[0] in MR:
                            if j[1] == (index + 1):
                                relate_word_position = j[2]
                                if pos[relate_word_position - 1][1] in adj_pos:
                                    o = tokenize[relate_word_position - 1]
                                    list_opinion.append(o)
                                    # O-->O-dep-->T
                            elif j[2] == (index + 1):
                                relate_word_position = j[1]
                                for j in dependency:
                                    if j[0] in MR:
                                        if j[2] != (index + 1) and j[1] == relate_word_position:
                                            relate_word_position = j[2]
                                            if pos[relate_word_position-1][1] in adj_pos:
                                                o = tokenize[relate_word_position - 1]
                                                list_opinion.append(o)
                                                # O-->O-dep-->H<--T-dep<--T
    list_opinion = list(set(list_opinion))
    return list_opinion


def rule3(text, target_file):
    list_target = []
    tokenize, pos, dependency = SC(text)
    tokenize = np.array(tokenize)
    for index, i in enumerate(pos):
        if i[1] in noun_pos:
            with open(target_file) as f:
                if i[0] in f.read():
                    f.close()
                    for j in dependency:
                        if j[1] == (index + 1) and j[0] == "conj":
                            relate_word_position = j[2]
                            if pos[relate_word_position - 1][1] in noun_pos:
                                t = tokenize[relate_word_position - 1]
                                list_target.append(t)
                                # Ti(j) → Ti(j)-Dep → Tj(i)
                        if j[0] in MR and j[2] == (index + 1):
                            relate_word_position = j[1]
                            for j in dependency:
                                if j[0] in MR:
                                    if j[1] == relate_word_position and j[2] != (index + 1):
                                        relate_word_position = j[2]
                                        if pos[relate_word_position - 1][1] in noun_pos:
                                            t = tokenize[relate_word_position - 1]
                                            list_target.append(t)
                                            # Ti →Ti-Dep→ H ←Tj-Dep← Tj
    list_target = list(set(list_target))
    return list_target


def rule4(text, opinion_file):
    list_opinion = []
    tokenize, pos, dependency = SC(text)
    tokenize = np.array(tokenize)
    for index, i in enumerate(pos):
        if i[1] in adj_pos:
            with open(opinion_file) as f:
                if i[0] in f.read():
                    for j in dependency:
                        if j[1] == (index + 1) and j[0] == "conj":
                            relate_word_position = j[2]
                            if pos[relate_word_position - 1][1] in adj_pos:
                                o = tokenize[relate_word_position - 1]
                                list_opinion.append(o)
                                # Oi(j) →Oi(j)-Dep→ Oj(i)
                        if j[0] in MR and j[2] == (index + 1):
                            relate_word_position = j[1]
                            for j in dependency:
                                if j[0] in MR:
                                    if j[1] == relate_word_position and j[2] != (index + 1):
                                        relate_word_position = j[2]
                                        if pos[relate_word_position - 1][1] in adj_pos:
                                            o = tokenize[relate_word_position - 1]
                                            list_opinion.append(o)
                                            # Oi →Oi-Dep→ H ←Oj-Dep← Oj
    list_opinion = list(set(list_opinion))
    return list_opinion




