import rule
import pandas as pd
from nltk.tokenize import sent_tokenize
import re
from preprocessing import preprocessing


# combine word from negative and positive file
def seed_opinion(opinion_file):
    list_opinion = []
    positive_opinion_fp = "opinion-lexicon/positive-words.txt"
    negative_opinion_fp = "opinion-lexicon/negative-words.txt"
    f = open(positive_opinion_fp)
    g = open(negative_opinion_fp)
    for word in f.readlines()[30:]:
        list_opinion.append(word.replace("\n", ""))
    for word in g.readlines()[30:]:
        list_opinion.append(word.replace("\n", ""))
    f.close()
    g.close()
    list_opinion = list(set(list_opinion))
    with open(opinion_file, "w") as f:
        for n in list_opinion:
            f.write(n + "\n")
    f.close()


def double_propagation(reviews, target_file, opinion_file):
    for review in reviews:
        review = preprocessing(review)
        print(review)
        if len(review.split()) > 1:
            sentences = sent_tokenize(str(review))
            for sentence in sentences:
                print(sentence)
                targets = rule.rule1(sentence, opinion_file)
                print("Extracted targets by Rule 1:", targets)
                with open(target_file, "a+") as f:
                    for n in targets:
                        f.write(n + "\n")
                f.close()

                # opinions = rule.rule4(sentence, opinion_file)
                # print("Extracted opinions by Rule 4: ", opinions)
                # with open(opinion_file, "r+") as f:
                #     for n in opinions:
                #         if n not in f.read():
                #             f.write(n + "\n")
                # f.close()

    for review in reviews:
        review = preprocessing(review)
        print(review)
        number_of_words = len(review.split())
        if number_of_words > 2:
            sentences = sent_tokenize(str(review))
            for sentence in sentences:
                print(sentence)

                # targets = rule.rule3(sentence, target_file)
                # print("Extracted targets by Rule 3:", targets)
                # with open(target_file, "r+") as f:
                #     for n in targets:
                #         f.write(n + "\n")
                # f.close()

                opinions = rule.rule2(sentence, target_file)
                print("Extracted opinions by Rule 2:", opinions)
                with open(opinion_file, "a+") as f:
                    for n in opinions:
                        if n not in f.read():
                            f.write(n + "\n")
                f.close()

