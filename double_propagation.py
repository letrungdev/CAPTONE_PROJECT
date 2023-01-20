import rule
import pandas as pd
from nltk.tokenize import sent_tokenize


data_file = "Data/Amazon_Mobile.csv"
opinion_file = "extracted/opinion.txt"
target_file = "extracted/target.txt"


def seed_opinion():
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


f = open("extracted/target.txt")
g = open("extracted/opinion.txt")


def preprocessing(text):
    text = text.lower()
    return text


def double_propagation(file):
    df = pd.read_csv(file)
    print("Read file: Done")
    reviews = df["Reviews"].tolist()[:10]

    for review in reviews:
        review = preprocessing(review)
        print(review)
        number_of_words = len(review.split())
        if number_of_words > 2:
            sentences = sent_tokenize(str(review))
            for sentence in sentences:
                print(sentence)
                targets = rule.rule1(sentence, opinion_file)
                print(targets)
                with open(target_file, "r+") as f:
                    for n in targets:
                        if n not in f.read():
                            f.write(n + "\n")
                f.close()

                opinions = rule.rule4(sentence, opinion_file)
                print(opinions)
                with open(opinion_file, "r+") as f:
                    for n in opinions:
                        if n not in f.read():
                            f.write(n + "\n")
                f.close()

    for review in reviews:
        review = preprocessing(review)
        print(review)
        number_of_words = len(review.split())
        if number_of_words > 2:
            sentences = sent_tokenize(str(review))
            for sentence in sentences:
                print(sentence)
                targets = rule.rule3(sentence, target_file)
                print(targets)
                with open(target_file, "r+") as f:
                    for n in targets:
                        if n not in f.read():
                            f.write(n + "\n")
                f.close()

                opinions = rule.rule2(sentence, target_file)
                print(opinions)
                with open(opinion_file, "r+") as f:
                    for n in opinions:
                        if n not in f.read():
                            f.write(n + "\n")
                f.close()







# seed_opinion()
# double_propagation(data_file)


prunning(data_file, target_file)


def extract(data_file, target_file_final):
    df = pd.read_csv(data_file)
    print("Read file: Done")
    reviews = df["Reviews"].tolist()[:10]

    f = open(target_file_final)
    list_target = [line.replace("\n", "") for line in f.readlines()]
    target_frequency = {}
    for review in reviews:
        number_of_words = len(review.split())
        if number_of_words > 2:
            sentences = sent_tokenize(str(review))
            for sentence in sentences:

